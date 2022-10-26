from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from anjone.database import Base


class LoginLog(Base):
    __tablename__ = 'login_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(120))
    dev = Column(String(256))
    login_time = Column(DateTime)
    ip_addr = Column(String(120))
    access_way = Column(String(120))

    def __init__(self, phone=None, dev=None, ip_addr=None, access_way=None):
        self.phone = phone
        self.dev = dev
        self.ip_addr = ip_addr
        self.access_way = access_way
        self.login_time = datetime.utcnow()

    def __repr__(self):
        return f'<LoginLogin {self.phone}, {self.dev}, {self.ip_addr},{self.access_way}, {self.login_time}>'

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item
