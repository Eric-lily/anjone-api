from flask import Blueprint, request
from flask import Response as Resp

from anjone.common import Response
from anjone.common.Constant import AVATAR_PATH, MUSIC_IMAGE_PATH, VIDEO_IMAGE_PATH
from anjone.service import file_service
from anjone.utils.token import get_username, login_required

file_bp = Blueprint('file', __name__, url_prefix='/file')

IMAGE_FILES = ['jpg', 'png', 'jpeg', 'gif', 'webp']
AUDIO_FILES = ['mp3']
VIDEO_FILES = ['mp4']


# 文件映射
@file_bp.route('/avatar/<filename>')
def user_avatar(filename):
    with open(AVATAR_PATH + filename, 'rb') as f:
        avatar = f.read()
        resp = Resp(avatar, mimetype='image/*')
    return resp


@file_bp.route('/avatar/upload', methods=['POST'])
@login_required
def upload_avatar():
    username = get_username()
    avatar = request.files['avatar']
    # 判断图片格式
    if avatar and allowed_files(IMAGE_FILES, avatar.filename):
        return file_service.upload_avatar(avatar, username)
    return Response.create_error('1', '文件为空, 或者格式有误')


@file_bp.route('/music/<filename>')
def music_image(filename):
    with open(MUSIC_IMAGE_PATH + filename, 'rb') as f:
        image = f.read()
        resp = Resp(image, mimetype='image/*')
    return resp


@file_bp.route('/video/<filename>')
def video_image(filename):
    with open(VIDEO_IMAGE_PATH + filename, 'rb') as f:
        image = f.read()
        resp = Resp(image, mimetype='image/*')
    return resp


def allowed_files(file_types, filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in file_types
