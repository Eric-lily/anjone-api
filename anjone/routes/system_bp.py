from flask import Blueprint, session, request

from anjone.common import Response
from anjone.service import system_service

system_bp = Blueprint('system', __name__, url_prefix='/system')


@system_bp.route('/get_disk_usage', methods=['GET'])
def get_disk_usage():
    # if not session.get("username"):
    #     return Response.create_error('1', '用户未登录')
    return system_service.get_disk_usage()


@system_bp.route('/get_dev_info', methods=['GET'])
def get_dev_info():
    if not session.get("username"):
        return Response.create_error('1', '用户未登录')
    return system_service.get_dev_info()


@system_bp.route('get_version', methods=['GET'])
def get_version():
    if not session.get('username'):
        return Response.create_error('1', '用户未登录')
    return system_service.get_version()


@system_bp.route('/get_address', methods=['GET'])
def get_address():
    if not session.get('username'):
        return Response.create_error('1', '用户未登录')
    return system_service.get_address()
