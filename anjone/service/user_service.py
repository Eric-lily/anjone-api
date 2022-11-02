import json
import os

from flask import make_response, request
from werkzeug.security import generate_password_hash, check_password_hash

from anjone.common import Response
from anjone.common.Constant import default_admin_name, root_username, default_avatar
from anjone.common.Response import NotLogin
from anjone.database import mysql_db_session, db_session, engine
from anjone.models.mysql.User import User
from anjone.models.sqlite.LocalUser import LocalUser
from anjone.models.sqlite.LoginLog import LoginLog
from anjone.models.sqlite.SambUser import SambUser
from anjone.models.vo.LoginLogVo import LoginLogVo
from anjone.models.vo.UserInfoAndDevVo import UserInfoAndDevVo
from anjone.models.vo.UserInfoVo import UserInfoVo
from anjone.utils.cache import cache
from anjone.utils.common_util import get_login_dev
from anjone.utils.send_message import Message
from anjone.utils.token import generate_token


def register(phone):
    user = mysql_db_session.query(User).filter(User.phone == phone).first()
    if user:
        return Response.create_error(1, '用户已存在')
    # 发送验证码
    Message.send_message(phone)
    return Response.create_success('发送验证码成功')


def check_code(phone, code):
    real_code = cache.get(phone)
    if real_code == code:
        return Response.create_success("验证码正确")
    return Response.create_error(1, '验证码错误')


def set_password(phone, password):
    hash_password = generate_password_hash(password)

    # 将新注册的管理员放入到mysql数据库中
    new_user = User(phone, default_admin_name)
    mysql_db_session.add(new_user)
    mysql_db_session.commit()
    # mysql_db_session.add_all([user1,user2])
    # 将用户账号密码信息存在本地
    # todo 事务管理
    local_user = LocalUser(root_username, hash_password, phone, default_avatar, default_admin_name)
    db_session.add(local_user)
    db_session.commit()

    return Response.create_success("设置成功")


def login(phone, password):
    user = LocalUser.query.filter(LocalUser.phone == phone).first()
    if (not user) or not check_password_hash(user.password, password):
        return Response.create_error(1, "用户名或密码错误")
    # 将用户登录写入日志
    # todo 此处的ip地址并不真实，需要考虑反向代理的情况 request.remote_addr
    dev = get_login_dev()
    login_log = LoginLog(user.phone, dev, request.remote_addr, '浏览器')
    db_session.add(login_log)
    db_session.commit()
    # 存到session中
    token = generate_token(username=user.username)
    user_info_vo = UserInfoVo(user.username, user.phone, user.avatar, user.role, user.create_time)
    # todo 设备信息虚拟，之后需要进行补充
    devs = [{'dev': 'HDC-202-0001', 'time': '2022-9-16'}]
    uer_info_and_dev_vo = UserInfoAndDevVo(user_info_vo, devs)
    # 在响应头上加上token
    resp = make_response(Response.create_success(uer_info_and_dev_vo.to_json()))
    resp.headers['Authorization'] = token
    return resp


def reset_info(user_info, username):
    user = LocalUser.query.filter(LocalUser.username == username).first()
    # 检查username是否重复
    if user.username != user_info['username']:
        response = json.loads(check_field('username', user_info['username'])[0])
        if response['code'] == 0:
            user.username = user_info['username']
        else:
            return response
    # 检查phone是否重复
    if user.phone != user_info['phone']:
        # 不一致首先对比验证码
        real_code = cache.get(user_info['phone'])
        if real_code and real_code == user_info['code']:
            response = json.loads(check_field('phone', user_info['phone'])[0])
            if response['code'] == 0:
                user.phone = user_info['phone']
            else:
                return response
        else:
            return Response.create_error(1, '验证码错误')
    # 密码加密
    if user_info['password'] and len(user_info['password']) > 0:
        user.password = generate_password_hash(user_info['password'])
    db_session.commit()
    # 重设token
    token = generate_token(username)
    user_info = UserInfoVo(user.username, user.phone, user.avatar, user.role, user.create_time)
    resp = make_response(Response.create_success(user_info.to_json()))
    resp.headers['Authorization'] = token
    return resp


def get_code(phone):
    Message.send_message(phone)
    return Response.create_success("发送成功")


def check_field(key, value):
    user = None
    if key == 'phone':
        user = engine.execute('select * from local_user where phone = ?', [value]).first()
    elif key == 'username':
        user = engine.execute('select * from local_user where username = ?', [value]).first()
    if user:
        return Response.create_error(1, '%s重复' % key)
    return Response.create_success('check success')


def get_login_log(username):
    user = LocalUser.query.filter(LocalUser.username == username).first()
    if not user:
        return Response.create_error(NotLogin.code, NotLogin.message)
    logs = LoginLog.query.filter(LoginLog.phone == user.phone)
    res = []
    for i in logs:
        res.append(LoginLogVo(i).to_json())
    return Response.create_success(res)


def create_new_user(admin_user, phone, username, password):
    # 验证是否为管理员
    admin = LocalUser.query.filter(LocalUser.username == admin_user).first()
    if (not admin) or admin.role != default_admin_name:
        return Response.create_error(1, '非管理员不能进行该操作')
    # 验证用户名和电话号码是否重复
    resp = json.loads(check_field('username', username)[0])
    if resp['code'] != 0:
        return resp
    resp = json.loads(check_field('phone', phone)[0])
    if resp['code'] != 0:
        return resp
    user = LocalUser(username, generate_password_hash(password), phone, default_avatar, 'user')
    # samb用户名暂时使用user+电话后4位尾数
    samb_username = 'user'+phone[-4:]
    samb_user = SambUser(phone, samb_username)
    try:
        db_session.add(user)
        db_session.add(samb_user)
        db_session.commit()
        new_user = LocalUser.query.filter(LocalUser.username == username).first()
        # todo 执行脚本创建新的samba用户
        print(os.system('sh /root/anjone-api/anjone-api/shell/samba_user.sh ' + samb_username))
        user_info = UserInfoVo(new_user.username, new_user.phone, new_user.avatar, new_user.role, new_user.create_time)
        return Response.create_success(user_info.to_json())
    except Exception:
        return Response.create_error(1, '创建用户失败')


def get_users(admin_user):
    # 验证是否为管理员
    admin = LocalUser.query.filter(LocalUser.username == admin_user).first()
    if (not admin) or admin.role != default_admin_name:
        return Response.create_error(1, '非管理员不能进行该操作')
    users = LocalUser.query.filter(LocalUser.role == 'user')
    user_info_list = []
    for i in users:
        user_info = UserInfoVo(i.username, i.phone, i.avatar, i.role, i.create_time)
        user_info_list.append(user_info.to_json())
    return Response.create_success(user_info_list)