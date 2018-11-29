from app.views.mail_view import blue as mail_bp
from app.views.upload import bp as upload_bp

'''
    该模块不能被试图模块调用，否则会出现循环调用的问题
'''


def init_views(app):
    '''
    所有视图中蓝图注册的地方，
    该函数在app/__init__.py中被调用
    :param app:flask app
    :return:None
    '''
    app.register_blueprint(blueprint=mail_bp)
    app.register_blueprint(blueprint=upload_bp)

    return None
