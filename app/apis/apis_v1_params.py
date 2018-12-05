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