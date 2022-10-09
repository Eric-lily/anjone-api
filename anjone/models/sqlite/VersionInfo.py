from sqlalchemy import Column, String

from anjone.database import Base


class VersionInfo(Base):
    __tablename__ = 'version_info'
    dev_id = Column(String(50), primary_key=True)
    firmware_ver = Column(String(100))
    system_ver = Column(String(100))

    def __init__(self, dev_id=None, firmware_ver=None, system_ver=None):
        self.dev_id = dev_id
        self.firmware_ver = firmware_ver
        self.system_ver = system_ver

    def __repr__(self):
        return f'<VersionInfo {self.dev_id, self.firmware_ver, self.system_ver}>'

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item