from sqlalchemy import Column, String, DateTime

from anjone.database import Base


class DevInfo(Base):
    __tablename__ = 'dev_info'
    dev_id = Column(String(50), primary_key=True)
    model_id = Column(String(20))
    cpu_info = Column(String(255))
    memory = Column(String(255))
    flash_memory = Column(String(255))
    disk_info = Column(String(255))
    stat = Column(String(255))
    bluetooth = Column(String(255))
    wifi = Column(String(255))
    cable = Column(String(255))
    usb = Column(String(255))
    hdmi = Column(String(255))
    zigbee = Column(String(255))
    screen = Column(String(255))
    speaker = Column(String(255))
    create_time = Column(DateTime)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        item['create_time'] = self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        return item
