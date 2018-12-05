
from flask_restful import Resource, marshal_with

from app.apis.apis_v1_params import *
from app.apis.apis_v1_results import *


class DemoAPI(Resource):
    #get_fields定义在apis_v1_results.py中，定义了返回参数的格式
    @marshal_with(get_fields)
    def get(self):
        #获取参数，定义在apis_v1_params.py中，通过reqparse模块获取request中传入的参数
        params = demo_params.parse_args()
        arg_03 = params.get('arg_03')

        if arg_03:

            return {
                'msg': 'get请求成功',
                'data': [arg_03, arg_03, arg_03, arg_03]
            }
        else:
            return {
                'code': 1,
                'msg': 'get请求失败'
            }

    @marshal_with(public_fields)
    def post(self):
        params = demo_params.parse_args()
        arg_01 = params.get('arg_01')
        arg_02 = params.get('arg_02')

        if arg_01 and arg_02:

            return {
                'msg': 'post请求成功',
                'data': ("arg_01:%s,arg_02:%s" % (arg_01,arg_02))
            }

        else:
            return {
                'code': 1,
                'msg': 'post请求失败'
            }

    @marshal_with(public_fields)
    def put(self):
        params = demo_params.parse_args()
        data = params.get('data')
        print(data)

        if True:

            return {
                'msg': 'post请求成功',
            }

        else:
            return {
                'code': 1,
                'msg': 'post请求失败',
            }


    @marshal_with(public_fields)
    def delete(self):
        pass

    @marshal_with(public_fields)
    def update(self):
        pass
