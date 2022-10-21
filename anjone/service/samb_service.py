import io

from anjone.common import Response
from anjone.utils.Samb import Samb, SambService
from flask import Response as Resp

IMAGE_TYPES = ['jpg', 'png', 'jpeg', 'gif', 'webp']
AUDIO_FILES = ['mp3']
VIDEO_FILES = ['mp4']


def start_service(username):
    # 建立连接，并加入到连接池中
    server = Samb('chenhuaiyi', '123456', '192.168.31.207', 'share')
    is_conn = server.connect()
    if not is_conn:
        return Response.create_error(1, 'samba connect error')
    if username in SambService:
        del SambService[username]
    SambService[username] = server
    # 查询个人目录下的主文件夹
    folder_list = server.get_aside()
    return Response.create_success(folder_list)


def stop_service(username):
    # 断开连接, 事访内存
    if (username in SambService) and SambService[username]:
        SambService[username].disconnect()
        del SambService[username]
    return Response.create_success('samba disconnect success')


def enter(username, filename, type):
    if not (username in SambService) or not SambService[username]:
        return Response.create_error(1, 'samba connect error')
    # todo 还需考虑如果filename是文件的情况
    server = SambService[username]
    if type == 'dir':
        folder_list = server.enter_dir(filename)
        return Response.create_success(folder_list)
    elif type == 'image':
        bytes = server.get_bytes(filename)
        resp = Resp(bytes, mimetype='image/*')
        return resp
    elif type == 'audio':
        bytes = server.get_bytes(filename)
        resp = Resp(bytes, mimetype='audio/mpeg')
        return resp
    elif type == 'video':
        bytes = server.get_bytes(filename)
        resp = Resp(bytes, mimetype='video/mp4')
        return resp
    else:
        return Response.create_success('This file type is not currently supported')


def check_file(username, filename):
    if not (username in SambService) or not SambService[username]:
        return Response.create_error(1, 'samba connect error')
        # todo 还需考虑如果filename是文件的情况
    server = SambService[username]
    files = server.get_current_files()
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
    if not (username in SambService) or not SambService[username]:
        return Response.create_error(1, 'samba connect error')
    server = SambService[username]
    # todo 对于非文件夹的文件如何处理
    return Response.create_success(server.enter_abs_file(filepath))


def back_dir(username):
    if not (username in SambService) or not SambService[username]:
        return Response.create_error(1, 'samba connect error')
    server = SambService[username]
    folder_list = server.back_dir()
    if not folder_list:
        return Response.create_error(1, 'you can not back now')
    return Response.create_success(folder_list)


def allowed_files(file_types, filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in file_types


def upload_file(username, recv_file):
    if not (username in SambService) or not SambService[username]:
        return Response.create_error(1, 'samba connect error')
    server = SambService[username]
    # 获取文件流和文件名
    with io.BytesIO() as file:
        file.write(recv_file.read())
        file.seek(0)
        filename = recv_file.filename
        res = server.upload_file(file, filename)
        if res :
            return Response.create_success(server.get_current_files_info())
        return Response.create_error(1, "Failed to upload file")


def delete_file(username, filename):
    if not (username in SambService) or not SambService[username]:
        return Response.create_error(1, 'samba connect error')
    server = SambService[username]
    # todo 还需要考虑删除的文件为文件夹的情况
    # 查找是否存在该文件
    folders = server.get_current_files()
    flag = False
    for i in folders:
        if i.filename == filename:
            flag = True
            break
    if flag:
        if server.delete_file(filename):
            return Response.create_success(server.get_current_files_info())
        return Response.create_error(1, "Failed to delete file")
    return Response.create_error(1, "Failed to delete file")