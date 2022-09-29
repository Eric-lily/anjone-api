from flask import Blueprint, request

from anjone.common import Exceptions
from anjone.service import user_service

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