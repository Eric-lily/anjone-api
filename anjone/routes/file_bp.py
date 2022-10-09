from flask import Blueprint, Response

from anjone.common.Constant import AVATAR_PATH

file_bp = Blueprint('file', __name__, url_prefix='/file')


# 文件映射
@file_bp.route('/avatar/<filename>')
def user_avatar(filename):
    with open(AVATAR_PATH+filename, 'rb') as f:
        avatar = f.read()
        resp = Response(avatar, mimetype='image/*')
    return resp