class UserInfoVo:
    def __init__(self, username=None, phone=None, avatar=None, role=None, create_time=None):
        self.username = username
        self.phone = phone
        self.avatar = avatar
        self.role = role
        self.create_time = create_time.strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return f'<User {self.username}, {self.phone}, {self.avatar}, {self.role} ,{self.create_time}>'

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item