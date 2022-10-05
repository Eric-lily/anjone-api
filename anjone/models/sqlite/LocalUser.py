from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from anjone.database import Base


class LocalUser(Base):
    __tablename__ = 'local_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(120), unique=True)
    password = Column(String(120))
    phone = Column(String(120), unique=True)
    create_time = Column(DateTime)
    update_time = Column(DateTime)

    def __init__(self, username=None, password=None, phone=None):
        self.username = username
        self.password = password
        self.phone = phone
        self.create_time = datetime.utcnow()
        self.update_time = datetime.utcnow()

    def __repr__(self):
        return f'<User {self.username}, {self.phone}>'

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item