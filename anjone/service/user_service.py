import json

from flask import session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from anjone.common import Response
from anjone.database import mysql_db_session, db_session, engine
from anjone.models.sqlite.LocalUser import LocalUser
from anjone.models.mysql.User import User
from anjone.models.vo.UserInfoVo import UserInfoVo
from anjone.utils.cache import cache
from anjone.utils.send_message import Message

default_admin_name = 'admin'
root_username = 'root'


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
    local_user = LocalUser(root_username, hash_password, phone, 'https://xxx.jpg', default_admin_name)
    db_session.add(local_user)
    db_session.commit()

    return Response.create_success("设置成功")


def login(phone, password):
    user = LocalUser.query.filter(LocalUser.phone == phone).first()
    # todo 加密处理
    if (not user) or not check_password_hash(user.password, password):
        return Response.create_error(1, "用户名或密码错误")
    # 存到session中
    session['username'] = user.username
    user_info_vo = UserInfoVo(user.username, user.phone, user.avatar, user.role, user.create_time)
    return Response.create_success(user_info_vo.to_json())


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
    # 重设session
    session.pop('username')
    session['username'] = user.username
    user_info = UserInfoVo(user.username, user.phone, user.avatar, user.role, user.create_time)
    return Response.create_success(user_info.to_json())


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
