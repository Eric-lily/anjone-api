from anjone.utils.common_util import format_time


class FileInfoVo:
    def __init__(self, i):
        self.filename = i.filename
        self.file_size = i.file_size
        self.read_only = i.isReadOnly
        self.is_dir = i.isDirectory
        self.create_time = format_time(i.create_time)
        self.last_access_time = format_time(i.last_access_time)
        self.last_write_time = format_time(i.last_write_time)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item