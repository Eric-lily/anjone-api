from sqlalchemy import Column, Integer, String

from anjone.database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    phone = Column(String(50), unique=True)
    password = Column(String(120), unique=True)

    def __init__(self, phone=None, password=None):
        self.phone = phone
        self.password = password

    def __repr__(self):
        return f'<User {self.phone}, {self.password}>'

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item
