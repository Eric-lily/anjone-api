from flask import Blueprint, request

from anjone.service import samb_service
from anjone.utils.Samb import lock
from anjone.utils.token import get_username, login_required, get_username_from_parameter

samb_bp = Blueprint('samb', __name__, url_prefix='/samb')


# 开启samba服务
@samb_bp.route('/start', methods=['POST', 'GET'])
@login_required
def start_service():
    username = get_username()
    lock.acquire()
    res = samb_service.start_service(username)
    lock.release()
    return res


# 关闭samba服务
@samb_bp.route('/stop', methods=['POST', 'GET'])
@login_required
def stop_service():
    username = get_username()
    lock.acquire()
    res = samb_service.stop_service(username)
    lock.release()
    return res


# 进入文件
@samb_bp.route('/enter/<filename>', methods=['POST', 'GET'])
def enter(filename):
    username = get_username_from_parameter()
    type = request.args.get('type')
    lock.acquire()
    res = samb_service.enter(username, filename, type)
    lock.release()
    return res


# 进入文件前先检查
@samb_bp.route('/check/<filename>', methods=['POST'])
@login_required
def check(filename):
    username = get_username()
    lock.acquire()
    res = samb_service.check_file(username, filename)
    lock.release()
    return res


# 从绝对路径进入文件夹
@samb_bp.route('/enter_abs', methods=['POST'])
@login_required
def enter_abs():
    username = get_username()
    filepath = request.form['filepath']
    lock.acquire()
    res = samb_service.enter_abs(username, filepath)
    lock.release()
    return res


# 返回上一级文件夹
@samb_bp.route('/back', methods=['POST'])
@login_required
def back_dir():
    username = get_username()
    lock.acquire()
    res = samb_service.back_dir(username)
    lock.release()
    return res


# 上传文件
@samb_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    username = get_username()
    recv_file = request.files.getlist('file')
    lock.acquire()
    res = samb_service.upload_file(username, recv_file)
    lock.release()
    return res


# 删除文件
@samb_bp.route('/delete', methods=['POST'])
@login_required
def delete_file():
    filename = request.form['filename']
    username = get_username()
    lock.acquire()
    res = samb_service.delete_file(username, filename)
    lock.release()
    return res


# 创建文件夹
@samb_bp.route('/create_dir', methods=['POST'])
@login_required
def create_dir():
    dir_name = request.form['dir_name']
    username = get_username()
    lock.acquire()
    res = samb_service.create_dir(username, dir_name)
    lock.release()
    return res


# 文件重命名
@samb_bp.route('/rename', methods=['POST'])
@login_required
def rename():
    old_name = request.form['old_name']
    new_name = request.form['new_name']
    username = get_username()
    lock.acquire()
    res = samb_service.rename(username, old_name, new_name)
    lock.release()
    return res


# 查看文件详情
@samb_bp.route('/file_info/<filename>', methods=['POST', 'GET'])
@login_required
def get_file_info(filename):
    username = get_username()
    lock.acquire()
    res = samb_service.get_file_info(username, filename)
    lock.release()
    return res


# 刷新
@samb_bp.route('refresh', methods=['POST', 'GET'])
@login_required
def refresh():
    username = get_username()
    lock.acquire()
    res = samb_service.refresh(username)
    lock.release()
    return res
