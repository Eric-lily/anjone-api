from flask import Blueprint, session

from anjone.common import Response
from anjone.common.Response import NotLogin
from anjone.service import samb_service

samb_bp = Blueprint('samb', __name__, url_prefix='/samb')


@samb_bp.route('/start', methods=['POST', 'GET'])
def start_service():
    username = session.get('username')
    if not session.get('username'):
        return Response.create_error(NotLogin.code, NotLogin.message)
    return samb_service.start_service(username)


@samb_bp.route('/stop', methods=['POST', 'GET'])
def stop_service():
    username = session.get('username')
    if not session.get('username'):
        return Response.create_error(NotLogin.code, NotLogin.message)
    return samb_service.stop_service(username)


@samb_bp.route('/enter/<filename>', methods=['POST'])
def enter(filename):
    username = session.get('username')
    if not session.get('username'):
        return Response.create_error(NotLogin.code, NotLogin.message)
    return samb_service.enter(username, filename)


@samb_bp.route('/back', methods=['POST'])
def back_dir():
    username = session.get('username')
    if not session.get('username'):
        return Response.create_error(NotLogin.code, NotLogin.message)
    return samb_service.back_dir(username)
