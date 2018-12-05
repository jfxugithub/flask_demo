import os

from flask import Flask

from app import settings
from app.apis.apis_v1_url import init_apis_v1
from app.ext import init_ext
from app.views import init_views
from log.basic_log import init_logging

"""
    此模块只给manager调用，其它模块不能调用，不然会出现循环调用
"""


def create_app(config='default'):
    '''
    创建flask app，并加载配置，初始化外部插件，views和数据库等
    该函数被manage模块调用
    :param config:选择开发环境，测试环境和线上环境
    :return:flask app
    '''

    # 日志初始化
    init_logging(os.path.join(settings.BASEDIR, "log/log_config.yaml"))

    app = Flask('demo', static_folder=settings.STATICPATH, template_folder=settings.TEMPLATESPATH)

    app.config.from_object(settings.ENV.get(config))

    init_ext(app)

    init_views(app)

    init_apis_v1(app)

    return app
