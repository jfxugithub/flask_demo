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


