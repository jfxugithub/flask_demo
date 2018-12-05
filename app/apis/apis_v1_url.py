from app.apis.apis_v1 import *
from flask_restful import Api

api = Api()


def init_apis_v1(app):
    '''
    在app初始化的时候调用
    :param app:
    :return:
    '''
    api.init_app(app)
    return None


'''
为每个api接口分配路由
'''
# 分配路由
api.add_resource(DemoAPI, "/demo")
