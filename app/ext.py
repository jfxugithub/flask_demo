import os
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache

from app import settings

db = SQLAlchemy()

migrate = Migrate()

sess = Session()

cache = Cache(config=settings.CACHES.get(os.getenv('CACHE_CONFIG') or 'default'))

def init_ext(app):
    '''
    所有外部插件统一初始化的地方
    :param app: flask app
    :return: None
    '''

    db.init_app(app)

    migrate.init_app(app=app,db=db)

    sess.init_app(app=app)

    cache.init_app(app=app)

    return None