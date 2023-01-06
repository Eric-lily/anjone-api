from flask import Blueprint

from anjone.service import media_service
from anjone.utils.token import login_required

media_bp = Blueprint('media', __name__, url_prefix='/media')


@media_bp.route('/music/get_all', methods=['GET'])
@login_required
def get_all_music():
    return media_service.get_all_music()


@media_bp.route('/video/get_all')
@login_required
def get_all_video():
    return media_service.get_all_video()
