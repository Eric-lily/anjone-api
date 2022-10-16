import io

from anjone.utils.Samb import Samb, SambService
from anjone.common import Response

IMAGE_TYPES = ['jpg', 'png', 'jpeg', 'gif', 'webp']


def start_service(username):
    # 建立连接，并加入到连接池中
    server = Samb('chenhuaiyi', '123456', '192.168.2.151', 'share')
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


def enter(username, filename):
    if not (username in SambService) or not SambService[username]:
        return Response.create_error(1, 'samba connect error')
    # todo 还需考虑如果filename是文件的情况
    server = SambService[username]
    files = server.get_current_files()
    for i in files:
        # 文件夹
        if i.filename == filename and i.isDirectory:
            folder_list = server.enter_dir(filename)
            return Response.create_success(folder_list)
        # 图片
        if i.filename == filename and is_image(filename):
            base64_code = server.get_image_base64(filename)
            # 给图片加上头部
            base64_code = 'data:image/jpeg;base64,' + str(base64_code)[2:-1]
            return Response.create_success(base64_code)
    return Response.create_error(1, 'is not directory')


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


def is_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in IMAGE_TYPES
