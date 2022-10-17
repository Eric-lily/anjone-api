import base64
import io
import os

from smb.SMBConnection import SMBConnection

from anjone.models.vo.FileInfoVo import FileInfoVo

SambService = {}


def reset_folders(folders):
    del folders[0]
    del folders[0]
    return folders


class Samb:
    def __init__(self, username=None, password=None, server_ip=None, folder=None):
        self.username = username
        self.password = password
        self.server_ip = server_ip
        self.folder = folder
        self.coon = None
        # 记录当前的目录位置, /photos
        self.current_folder = None

    def connect(self):
        self.conn = SMBConnection(username=self.username, password=self.password, my_name='', remote_name='',
                                  use_ntlm_v2=True,
                                  is_direct_tcp=True)
        try:
            self.conn.connect(self.server_ip, 139)
        except Exception as e:
            return False
        return True

    def disconnect(self):
        self.conn.close()
        self.coon = None

    def get_aside(self):
        folder_list = []
        folders = self.conn.listPath(self.folder, '/')
        self.current_folder = '/'
        for i in folders:
            folder = FileInfoVo(i).to_json()
            folder_list.append(folder)
        return reset_folders(folder_list)

    def get_current_files(self):
        return self.conn.listPath(self.folder, self.current_folder)

    def enter_dir(self, dirname):
        folder_list = []
        self.current_folder = self.current_folder + dirname + '/'
        folders = self.conn.listPath(self.folder, self.current_folder)
        for i in folders:
            folder = FileInfoVo(i).to_json()
            folder_list.append(folder)
        return reset_folders(folder_list)

    def enter_abs_file(self, filepath):
        folder_list = []
        self.current_folder = filepath + '/'
        folders = self.conn.listPath(self.folder, filepath + '/')
        for i in folders:
            folder = FileInfoVo(i).to_json()
            folder_list.append(folder)
        return reset_folders(folder_list)

    def back_dir(self):
        # 截取掉最后一个文件夹
        index = self.current_folder.rfind(r'/', 0, -1)
        if index == -1:
            return False
        self.current_folder = self.current_folder[0: index + 1]
        folder_list = []
        folders = self.get_current_files()
        for i in folders:
            folder = FileInfoVo(i).to_json()
            folder_list.append(folder)
        return reset_folders(folder_list)

    def get_image_base64(self, image_name):
        with io.BytesIO() as file:
            self.conn.retrieveFile(self.folder, os.path.join(self.current_folder, image_name), file)
            file.seek(0)
            return base64.b64encode(file.read())
