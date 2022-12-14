from anjone.common import Response
from anjone.database import mysql_db_session
from anjone.models.User import User
from anjone.utils.cache import cache
from anjone.utils.send_message import Message


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
    new_user = User(phone, password)
    # todo 加密处理
    # mysql_db_session.add_all([user1,user2])
    mysql_db_session.add(new_user)
    mysql_db_session.commit()
    return Response.create_success("设置成功")


def login(phone, password):
    user = mysql_db_session.query(User).filter(User.phone == phone).first()
    # todo 加密处理
    if (not user) or user.password != password:
        return Response.create_error(1, "用户名或密码错误")
    return Response.create_success("登录成功")