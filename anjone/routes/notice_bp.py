from flask import Blueprint

from anjone.service import notice_service
from anjone.utils.token import login_required

notice_bp = Blueprint('notice', __name__, url_prefix='/notice')


@notice_bp.route('/delete_all', methods=['POST'])
@login_required
def delete_all():
    return notice_service.delete_all()


# 获取通知，进行轮询
@notice_bp.route('/get_notice', methods=['GET'])
@login_required
def get_notice():
    return notice_service.get_notice()