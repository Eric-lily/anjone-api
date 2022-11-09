import io

from flask import Response as Resp

from anjone.common import Response
from anjone.common.Constant import default_samba_ip
from anjone.models.sqlite.LocalUser import LocalUser
from anjone.models.sqlite.SambUser import SambUser
from anjone.models.vo.FileInfoVo import FileInfoVo
from anjone.utils.Samb import Samb, SambService, del_conn, set_conn, has_conn, get_conn, lock

IMAGE_TYPES = ['jpg', 'png', 'jpeg', 'gif', 'webp']
AUDIO_FILES = ['mp3']
VIDEO_FILES = ['mp4']


def start_service(username):
    # 建立连接，并加入到连接池中
    user = LocalUser.query.filter(LocalUser.username == username).first()
    samb_user = SambUser.query.filter(SambUser.phone == user.phone).first()
    # 判断是否创建了对应的samba用户
    if not samb_user:
        return Response.create_error(1, 'no samba user')
    server = Samb(samb_user.username, samb_user.password, default_samba_ip, samb_user.username)
    is_conn = server.connect()
    if not is_conn:
        return Response.create_error(1, 'samba connect error')
    # 删除已有连接,设置新的连接
    del_conn(username)
    set_conn(username, server)
    # 查询个人目录下的主文件夹
    folder_list = server.get_aside()
    return Response.create_success(folder_list)


def stop_service(username):
    # 断开连接, 事访内存
    if has_conn(username):
        get_conn(username).disconnect()
        del_conn(username)
        # 释放锁
        lock.release()
    return Response.create_success('samba disconnect success')


def enter(username, filename, type):
    if has_conn(username):
        return Response.create_error(1, 'samba connect error')
    # todo 还需考虑如果filename是文件的情况
    server = get_conn(username)
    if type == 'dir':
        folder_list = server.enter_dir(filename)
        # 释放锁
        lock.release()
        return Response.create_success(folder_list)
    elif type == 'image':
        bytes = server.get_bytes(filename)
        resp = Resp(bytes, mimetype='image/*')
        # 释放锁
        lock.release()
        return resp
    elif type == 'audio':
        bytes = server.get_bytes(filename)
        resp = Resp(bytes, mimetype='audio/mpeg')
        # 释放锁
        lock.release()
        return resp
    elif type == 'video':
        bytes = server.get_bytes(filename)
        resp = Resp(bytes, mimetype='video/mp4')
        # 释放锁
        lock.release()
        return resp
    else:
        # 释放锁
        lock.release()
        return Response.create_success('This file type is not currently supported')


def check_file(username, filename):
    if has_conn(username):
        return Response.create_error(1, 'samba connect error')
        # todo 还需考虑如果filename是文件的情况
    server = get_conn(username)
    files = server.get_current_files()
    # 释放锁
    lock.release()
    for i in files:
        if i.filename == filename:
            # 文件夹
            if i.isDirectory:
                return Response.create_success('dir')
            # 图片
            if allowed_files(IMAGE_TYPES, filename):
                return Response.create_success('image')
            # 音频
            if allowed_files(AUDIO_FILES, filename):
                return Response.create_success('audio')
            # 视频
            if allowed_files(VIDEO_FILES, filename):
                return Response.create_success('video')
            else:
                return Response.create_success('other')
    return Response.create_error(1, 'no file')


def enter_abs(username, filepath):
    if has_conn(username):
        return Response.create_error(1, 'samba connect error')
    server = get_conn(username)
    # todo 对于非文件夹的文件如何处理
    folders = server.enter_abs_file(filepath)
    # 释放锁
    lock.release()
    return Response.create_success(folders)


def back_dir(username):
    if has_conn(username):
        return Response.create_error(1, 'samba connect error')
    server = get_conn(username)
    folder_list = server.back_dir()
    # 释放锁
    lock.release()
    if not folder_list:
        return Response.create_error(1, 'you can not back now')
    return Response.create_success(folder_list)


def allowed_files(file_types, filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in file_types


def upload_file(username, recv_file):
    if has_conn(username):
        return Response.create_error(1, 'samba connect error')
    server = get_conn(username)
    # 获取文件流和文件名, flag存储未成功上传的文件名
    flag = True
    for i in recv_file:
        with io.BytesIO() as file:
            file.write(i.read())
            file.seek(0)
            filename = i.filename
            if not server.upload_file(file, filename):
                flag = False
    if flag:
        folders = server.get_current_files_info()
        # 释放锁
        lock.release()
        return Response.create_success(folders)
    # 释放锁
    lock.release()
    return Response.create_error(1, "Failed to upload all files")


def delete_file(username, filename):
    if has_conn(username):
        return Response.create_error(1, 'samba connect error')
    server = get_conn(username)
    # 从字符串中拆分出文件名
    files = filename.split(',')
    for i in files:
        file_info = server.get_file_info(i)
        # 删除文件夹
        if file_info.isDirectory:
            server.delete_dir(server.get_current_folder() + i + '/')
        # 删除文件
        else:
            server.delete_file(i)
    # 释放锁
    lock.release()
    return Response.create_success(server.get_current_files_info())


def create_dir(username, dir_name):
    if has_conn(username):
        return Response.create_error(1, 'samba connect error')
    server = get_conn(username)
    if server.create_dir(dir_name):
        folders = server.get_current_files_info()
        # 释放锁
        lock.release()
        return Response.create_success(folders)
    # 释放锁
    lock.release()
    return Response.create_error(1, 'Failed to create directory')


def rename(username, old_name, new_name):
    if has_conn(username):
        return Response.create_error(1, 'samba connect error')
    server = get_conn(username)
    info = server.get_file_info(old_name)
    if info and server.rename(old_name, new_name):
        folders = server.get_current_files_info()
        # 释放锁
        lock.release()
        return Response.create_success(folders)
    # 释放锁
    lock.release()
    return Response.create_error(1, 'Rename failed')


def get_file_info(username, filename):
    if has_conn(username):
        return Response.create_error(1, 'samba connect error')
    server = get_conn(username)
    info = server.get_file_info(filename)
    if info:
        # 释放锁
        lock.release()
        return Response.create_success(FileInfoVo(info).to_json())
    # 释放锁
    lock.release()
    return Response.create_error(1, "No information about this file")


def refresh(username):
    if not has_conn(username):
        # 测试
        return Response.create_error(1, 'samba connect error')
    server = get_conn(username)
    # 释放锁
    lock.release()
    return Response.create_success(server.get_current_files_info())