from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

from anjone.common import Response
from anjone.database import mysql_db_session, db_session
from anjone.models.sqlite.LocalUser import LocalUser
from anjone.models.mysql.User import User
from anjone.utils.cache import cache
from anjone.utils.send_message import Message

default_admin_name = 'Admin'
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
    local_user = LocalUser(root_username,hash_password,phone)
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
    return Response.create_success("登录成功")