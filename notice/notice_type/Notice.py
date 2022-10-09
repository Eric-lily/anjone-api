class Notice:
    def __init__(self, title=None, create_time=None, content=None, type=None):
        self.title = title
        self.create_time = create_time
        self.content = content
        self.type = type

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item

    def __repr__(self):
        return f'<Notice {self.title, self.content, self.create_time, self.type}>'