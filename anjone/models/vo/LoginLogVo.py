from anjone.utils.common_util import format_time


class LoginLogVo:
    def __init__(self, login_log):
        self.phone = login_log.phone
        self.dev = login_log.dev
        self.ip_addr = login_log.ip_addr
        self.access_way = login_log.access_way
        self.login_time = login_log.login_time.strftime('%Y-%m-%d %H:%M:%S')

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item
