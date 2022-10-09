class LoginNotice:
    def __init__(self, create_time=None, dev=None, content=None):
        self.title = '新终端登录'
        self.create_time = create_time
        self.dev = dev
        self.content = content
        self.type = 'login'

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item

    def __repr__(self):
        return f'<LoginNotice {self.title, self.dev, self.content, self.create_time, self.type}>'
