import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'rockyrocky'  # SECRET_KEY 用于token等加密
    MYSQL_SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/anjone?charset=utf8'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////test.db'
    DEBUG = True


config = {
    'default': DevelopmentConfig
}

cache_config = {
    'CACHE_TYPE': 'simple'
}
