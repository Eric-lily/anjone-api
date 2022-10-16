from flask import Blueprint, session

from anjone.common import Response
from anjone.common.Response import NotLogin
from anjone.service import notice_service
from anjone.utils.token import login_required

notice_bp = Blueprint('notice', __name__, url_prefix='/notice')


@notice_bp.route('/delete_all', methods=['POST'])
@login_required
def delete_all():
    return notice_service.delete_all()