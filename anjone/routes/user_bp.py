from flask import Blueprint, request, session
from werkzeug.datastructures import ImmutableMultiDict

from anjone.common import Exceptions, Response
from anjone.common.Exceptions import ParameterNullException
from anjone.common.Response import NotLogin
from anjone.models.validate.UserInfoVal import UserInfoVal
from anjone.service import user_service
from anjone.utils.token import get_username, login_required

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/register', methods=['POST'])
def register():
    phone = request.form['phone']
    if not phone:
        raise Exceptions.ParameterNullException
    return user_service.register(phone)


@user_bp.route('/check_code', methods=['POST'])
def check_code():
    phone = request.form['phone']
    code = request.form['code']
    if not code:
        raise Exceptions.ParameterNullException
    return user_service.check_code(phone, code)


@user_bp.route('/set_password', methods=['POST'])
def set_password():
    phone = request.form['phone']
    password = request.form['password']
    if (not password) or (not phone):
        raise Exceptions.ParameterNullException
    return user_service.set_password(phone, password)


@user_bp.route('/login', methods=['POST'])
def login():
    phone = request.form['phone']
    password = request.form['password']
    if (not phone) or (not password):
        raise Exceptions.ParameterNullException
    return user_service.login(phone, password)


@user_bp.route('/reset_info', methods=['POST'])
@login_required
def reset_info():
    username = get_username()
    userinfo = request.get_json()
    # 表单验证，这里要使用ImmutableMultiDict封装dict
    if not UserInfoVal(ImmutableMultiDict(userinfo)).validate():
        raise ParameterNullException
    return user_service.reset_info(userinfo, username)


@user_bp.route('/get_code', methods=['POST'])
@login_required
def get_code():
    phone = request.form['phone']
    return user_service.get_code(phone)
