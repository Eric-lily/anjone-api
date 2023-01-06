from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime

from anjone.database import Base


class Video(Base):
    __tablename__ = 'video'
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_name = Column(String(50))
    publish_year = Column(String(50))
    preview_image = Column(String(100))
    resource = Column(String(200))

    def __init__(self, video_name=None, publish_year=None, preview_image=None, resource=None):
        self.video_name = video_name
        self.preview_image = preview_image
        self.publish_year = publish_year
        self.resource = resource

    def __repr__(self):
        return f'<Video {self.id, self.video_name, self.publish_time, self.preview_image, self.resource}>'

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item
