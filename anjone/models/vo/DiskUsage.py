class DiskUsage:
    def __init__(self, total=None, free = None, percent = None):
        self.total = total
        self.free = free
        self.percent = percent

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item
