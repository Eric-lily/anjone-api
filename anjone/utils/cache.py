from flask_caching import Cache

from configs.config import cache_config

cache = Cache(config=cache_config)


def configure_cache(app):
    global cache
    cache.init_app(app)