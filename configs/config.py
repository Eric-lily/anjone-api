import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'laowangaigebi'  # SECRET_KEY 用于session
    MYSQL_SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/anjone?charset=utf8'


# 开发环境
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////test.db'
    DEBUG = False


# 生产环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/firefly/project/test.db'
    DEBUG = False


config = {
    'default': ProductionConfig
}

cache_config = {
    'CACHE_TYPE': 'simple'
}
