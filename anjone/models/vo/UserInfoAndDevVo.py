class UserInfoAndDevVo:
    def __init__(self, user_info_vo=None, devs=None):
        self.username = user_info_vo.username
        self.phone = user_info_vo.phone
        self.avatar = user_info_vo.avatar
        self.role = user_info_vo.role
        self.create_time = user_info_vo.create_time
        self.devs = devs

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item