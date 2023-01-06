from sqlalchemy import Column, Integer, String

from anjone.database import Base


class Music(Base):
    __tablename__ = 'music'
    id = Column(Integer, primary_key=True, autoincrement=True)
    music_name = Column(String(100))
    album = Column(String(100))
    artist = Column(String(100))
    publish_year = Column(String(50))
    time = Column(String(50))
    rating = Column(Integer)
    preview_image = Column(String(200))
    resource = Column(String(200))

    def __init__(self, music_name, album, artist, publish_year, time, rating, preview_image, resource):
        self.music_name = music_name
        self.album = album
        self.artist = artist
        self.publish_year = publish_year
        self.time = time
        self.rating = rating
        self.preview_image = preview_image
        self.resource = resource

    def __repr__(self):
        return f'<Music {self.id, self.music_name, self.publish_time, self.preview_image, self.resource}>'

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item
