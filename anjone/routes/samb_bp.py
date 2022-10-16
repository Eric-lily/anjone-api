from flask import Blueprint, session, request

from anjone.common import Response
from anjone.common.Response import NotLogin
from anjone.service import samb_service
from anjone.utils.token import get_username, login_required

samb_bp = Blueprint('samb', __name__, url_prefix='/samb')


@samb_bp.route('/start', methods=['POST', 'GET'])
@login_required
def start_service():
    username = get_username()
    return samb_service.start_service(username)


@samb_bp.route('/stop', methods=['POST', 'GET'])
@login_required
def stop_service():
    username = get_username()
    return samb_service.stop_service(username)


@samb_bp.route('/enter/<filename>', methods=['POST'])
@login_required
def enter(filename):
    username = get_username()
    return samb_service.enter(username, filename)


@samb_bp.route('enter_abs', methods=['POST'])
@login_required
def enter_abs():
    username = get_username()
    filepath = request.form['filepath']
    return samb_service.enter_abs(username, filepath)


@samb_bp.route('/back', methods=['POST'])
@login_required
def back_dir():
    username = get_username()
    return samb_service.back_dir(username)
