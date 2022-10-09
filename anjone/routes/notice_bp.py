from flask import Blueprint, session

from anjone.common import Response
from anjone.common.Response import NotLogin
from anjone.service import notice_service

notice_bp = Blueprint('notice', __name__, url_prefix='/notice')


@notice_bp.route('/delete_all', methods=['POST'])
def delete_all():
    if not session.get('username'):
        return Response.create_error(NotLogin.code, NotLogin.message)
    return notice_service.delete_all()