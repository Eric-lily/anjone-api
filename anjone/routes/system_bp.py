from flask import Blueprint, session, request

from anjone.common import Response
from anjone.service import system_service
from anjone.utils.token import login_required, get_username

system_bp = Blueprint('system', __name__, url_prefix='/system')


@system_bp.route('/get_disk_usage', methods=['GET'])
@login_required
def get_disk_usage():
    return system_service.get_disk_usage()


@system_bp.route('/get_dev_info', methods=['GET'])
@login_required
def get_dev_info():
    return system_service.get_dev_info()


@system_bp.route('get_version', methods=['GET'])
@login_required
def get_version():
    return system_service.get_version()


@system_bp.route('/get_address', methods=['GET'])
@login_required
def get_address():
    return system_service.get_address()
