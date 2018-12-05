# Flask_Restful 模块

## api接口主体

app/apis/apis_v1.py

```
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

```

## api路由分配

app/apis/apis_v1_url.py

```
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

```

## api接口入参

app/apis/apis_v1_params.py

```
from flask_restful import reqparse

"""
api 接口接受参数
"""
demo_params = reqparse.RequestParser()
#从form中获取字符串arg_01
demo_params.add_argument('arg_01', type=str, location='form')
#从form中获取整数arg_01
demo_params.add_argument('arg_02', type=int, location='form')
#从get中获取字符串arg_01
demo_params.add_argument('arg_03', type=int, location='args')
#从json中获取参数data,action='append'表示获取多个值，如下示例
demo_params.add_argument('data', type=dict, location='json',action='append')

'''
{
	"data":[
		{
		"id":"1",
		"date":"2018-01-12",
		"destination":"杭州",
		"notes":"未付"
		},{
		"id":"1",
		"date":"2018-01-12",
		"destination":"杭州",
		"notes":"未付"
		}
	]
}
'''

############################
'''
add_argument:
        required=True  #表示请求中必须要有这个参数
        action='append' #表示有多个值
        dest='public_name' #给参数起别名，这样在获取变量的时候就可以使用别名获取了
        location = ['args','form','json','headers','values']    #指定一个或者多个获取参数的地方
        type=int/str/dict等 #指定参数类型
'''
```

## api返回参数定义

app/apis/apis_v1_results.py

```
from flask_restful import fields
'''
    自定义需要返回的数据格式
'''

public_fields = {
    'code': fields.Integer(default=0),
    'msg': fields.String(default='null'),
    'data': fields.String(default='null')
}

get_fields = {
    'code': fields.Integer(default=0),
    'msg': fields.String(default='null'),
    'data': fields.List(fields.Integer)
}

```



# 