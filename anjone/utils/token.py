from functools import wraps

from authlib.jose import jwt, JoseError
from flask import current_app, request

# 生成token
from anjone.common import Response
from anjone.common.Response import NotLogin


def generate_token(username):
    header = {'alg': 'HS256'}  # 签名算法
    key = current_app.config['SECRET_KEY']
    data = {'username': username}
    return jwt.encode(header=header, payload=data, key=key)


# 验证token
def validate_token(token):
    key = current_app.config['SECRET_KEY']
    try:
        data = jwt.decode(token, key)
        return data['username']
    except JoseError:
        return False


# 配置成装饰器
def login_required(view_func):
    @wraps(view_func)
    def verify_token(*args, **kwargs):
        try:
            # 在请求头上拿到token
            token = request.headers["Authorization"]
        except Exception:
            return Response.create_error(NotLogin.code, NotLogin.message)
        username = validate_token(token)
        if not username:
            return Response.create_error(NotLogin.code, NotLogin.message)
        return view_func(*args, **kwargs)
    return verify_token


def get_username():
    token = request.headers['Authorization']
    key = current_app.config['SECRET_KEY']
    data = jwt.decode(token, key)
    return data['username']


# 从parameter中获得token
def get_username_from_parameter():
    token = request.args.get('token')
    if token and validate_token(token):
        return validate_token(token)
    return Response.create_error(NotLogin.code, NotLogin.message)
