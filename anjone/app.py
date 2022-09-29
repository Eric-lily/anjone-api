from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from anjone.common.Exceptions import configure_exceptions
from anjone.database import db_session, init_db
from anjone.utils.cache import configure_cache
from configs.config import config as app_config


def create_app(config_name=None):
    """Create a Flask app."""

    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    configure_app(app, config_name)
    configure_blueprints(app)
    configure_exceptions(app)
    configure_cache(app)

    # 初始化数据库
    @app.cli.command('init-db')
    def init_db_cli():
        init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app


# 加载配置文件
def configure_app(app, config_name=None):
    if config_name:
        app.config.from_object(app_config['default'])


# 加载蓝图
def configure_blueprints(app):
    from anjone.routes.user_bp import user_bp
    app.register_blueprint(user_bp)
