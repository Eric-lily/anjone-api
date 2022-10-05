from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from anjone.database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    phone = Column(String(50), unique=True)
    name = Column(String(255))
    create_time = Column(DateTime)
    update_time = Column(DateTime)

    def __init__(self, phone=None, name=None):
        self.phone = phone
        self.name = name
        self.create_time = datetime.utcnow()
        self.update_time = datetime.utcnow()

    def __repr__(self):
        return f'<User {self.phone}, {self.name}>'

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item
