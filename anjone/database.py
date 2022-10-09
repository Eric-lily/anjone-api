from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from configs.config import config

engine = create_engine(config['default'].SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

engine_mysql = create_engine(config['default'].MYSQL_SQLALCHEMY_DATABASE_URI)
mysql_db_session = scoped_session(sessionmaker(autocommit=False,
                                               autoflush=False,
                                               bind=engine_mysql))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
    # 元数据上。否则你就必须在调用 init_db() 之前导入它们。
    from anjone.models.sqlite.LocalUser import LocalUser
    from anjone.models.sqlite.DevInfo import DevInfo
    from anjone.models.sqlite.VersionInfo import VersionInfo
    Base.metadata.create_all(bind=engine)
