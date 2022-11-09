import base64
import io
import os

from smb.SMBConnection import SMBConnection

from anjone.models.vo.FileInfoVo import FileInfoVo


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
            print(e)
            return False
        return True

    def disconnect(self):
        self.conn.close()
        self.coon = None

    def get_current_folder(self):
        return self.current_folder

    def get_file_info(self, filename):
        try:
            info = self.conn.getAttributes(self.folder, self.current_folder + filename)
            return info
        except Exception:
            return False

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

    def get_current_files_info(self):
        folders = self.conn.listPath(self.folder, self.current_folder)
        folder_list = []
        for i in folders:
            folder = FileInfoVo(i).to_json()
            folder_list.append(folder)
        return reset_folders(folder_list)

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
        folders = self.conn.listPath(self.folder, self.current_folder)
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

    def get_bytes(self, filename):
        with io.BytesIO() as file:
            self.conn.retrieveFile(self.folder, os.path.join(self.current_folder, filename), file)
            file.seek(0)
            return file.read()

    def upload_file(self, file, filename):
        try:
            self.conn.storeFile(self.folder, os.path.join(self.current_folder, filename), file)
            return True
        except Exception:
            return False

    def delete_file(self, filename):
        try:
            self.conn.deleteFiles(self.folder, self.current_folder + filename)
            return True
        except Exception:
            return False

    # 递归删除文件夹
    def delete_dir(self, path):
        for p in self.conn.listPath(self.folder, path):
            if p.filename != '.' and p.filename != '..':
                parent_path = path
                if not parent_path.endswith('/'):
                    parent_path += '/'
                # 递归位置
                if p.isDirectory:
                    self.delete_dir(parent_path + p.filename)
                else:
                    self.conn.deleteFiles(self.folder, parent_path + p.filename)
        # 删除掉文件夹内的文件后，再删除文件夹本身
        self.conn.deleteDirectory(self.folder, path)

    def create_dir(self, dir_name):
        try:
            self.conn.createDirectory(self.folder, self.current_folder + dir_name)
            return True
        except Exception:
            return False

    def rename(self, old_name, new_name):
        try:
            self.conn.rename(self.folder, self.current_folder + old_name, self.current_folder + new_name)
            return True
        except Exception:
            return False
