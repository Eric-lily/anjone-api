from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from anjone.common.Exceptions import configure_exceptions
from anjone.database import db_session, init_db, mysql_db_session
from anjone.utils.cache import configure_cache
from configs.config import config as app_config


def create_app(config_name=None):
    """Create a Flask app."""

    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    # 配置跨域
    CORS(app, supports_credentials=True)

    configure_app(app, config_name)
    configure_blueprints(app)
    configure_exceptions(app)
    configure_cache(app)

    # 初始化数据库
    @app.cli.command('init-db')
    def init_db_cli():
        init_db()

    # 应用关闭时关闭数据库连接
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        mysql_db_session.remove()
        db_session.remove()

    return app


# 加载配置文件
def configure_app(app, config_name=None):
    if not config_name:
        app.config.from_object(app_config['default'])


# 加载蓝图
def configure_blueprints(app):
    from anjone.routes.user_bp import user_bp
    from anjone.routes.system_bp import system_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(system_bp)
