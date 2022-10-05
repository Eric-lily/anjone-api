from flask import Blueprint, session

from anjone.common import Response
from anjone.service import system_service

system_bp = Blueprint('system', __name__, url_prefix='/system')


@system_bp.route('/get_disk_usage', methods=['GET'])
def get_disk_usage():
    # if not session.get("username"):
    #     return Response.create_error('1', '用户未登录')
    return system_service.get_disk_usage()
