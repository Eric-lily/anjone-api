from sqlalchemy import Column, Integer, String

from anjone.common.Constant import default_samba_pwd
from anjone.database import Base


class SambUser(Base):
    __tablename__ = 'samb_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(120), unique=True)
    username = Column(String(120), unique=True)
    password = Column(String(120), default=default_samba_pwd)

    def __init__(self, phone=None, username=None):
        self.phone = phone
        self.username = username

    def __repr__(self):
        return f'<SambUser {self.username}, {self.phone}>'

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item