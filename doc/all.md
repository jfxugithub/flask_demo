# 日志Loging模块

## loging配置

### Formatter

format：指定log最终输出的格式和内容

```
参数           ：作用
%(levelno)s   ：打印日志级别的数值
%(levelname)s ：打印日志级别的名称
%(pathname)s  ：打印当前执行程序的路径，其实就是sys.argv[0]
%(filename)s  ：打印当前执行程序名
%(funcName)s  ：打印日志的当前函数
%(lineno)d    ：打印日志的当前行号
%(asctime)s   ：打印日志的时间
%(thread)d    ：打印线程ID
%(threadName)s：打印线程名称
%(process)d   ：打印进程ID
%(message)s   ：打印日志信息

eg:
"formatters":{
    "simple":{
        "format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    },
    "mutil":{
        "format":"%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)d : %(message)s"
    },
},
```

### Handler

handlers:指定日志的输出方式

```
handler名称          ：作用

StreamHandler      	：日志输出到流，可以是sys.stderr，sys.stdout或者文件
FileHandler		   	：日志输出到文件
BaseRotatingHandler	：基本的日志回滚方式
RotatingHandler		：日志回滚方式，支持日志文件最大数量和日志文件回滚
TimeRotatingHandler	：日志回滚方式，在一定时间区域内回滚日志文件
SocketHandler		：远程输出日志到TCP/IP sockets
DatagramHandler		：远程输出日志到UDP sockets
SMTPHandler			：远程输出日志到邮件地址
SysLogHandler		：日志输出到syslog
NTEventLogHandler	：远程输出日志到Windows NT/2000/XP的事件日志
MemoryHandler		：日志输出到内存中的指定buffer
HTTPHandler			：通过"GET"或者"POST"远程输出到HTTP服务器

eg：
"handlers":{
		"console":{
            "class":"logging.StreamHandler",   
            "level":"DEBUG",
            "formatter":"simple",
            "stream":"ext://sys.stdout"
        },
        "info_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"INFO",
            "formatter":"simple",
            "filename":"info.log",    
            "maxBytes":"10485760",
            "backupCount":20,
            "encoding":"utf8"
        },
}        
```



### logger

​	提供日志接口，供应用代码使用，可以通过logging.getLogger(name)获取logger对象，如果不指定name则返回root对象，相同的name调用getLogger方法返回同一个logger对象。

```
日志等级 =	数字值 ：使用范围

FATAL	=	50	：致命错误
CRITICAL=	50	：特别糟糕的事情，如内存耗尽、磁盘空间为空，一般很少使用
ERROR	=	40	：发生错误时，如IO操作失败或者连接问题
WARNING	=	30	：发生很重要的事件，但是并不是错误时，如用户登录密码错误
INFO	=	20：处理请求或者状态变化等日常事务
DEBUG	=	10	：调试过程中使用DEBUG等级，如算法中每个循环的中间状态
NOTSET = 0
#设置log的级别（如果如果日志的级别低于设置的值，则log模块不会理会）
eg：
  "loggers":{
        "my_module":{
            "level":"INFO",                  #无法打印debug信息，其它信息都可以打印 
            "handlers":["info_file_handler"],
        }
    },
```





## 配置文件以及加载方式

### json配置文件

```
{
    "version":1,
    "disable_existing_loggers":false,
    "formatters":{
        "simple":{
            "format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers":{
        "console":{
            "class":"logging.StreamHandler",
            "level":"DEBUG",
            "formatter":"simple",
            "stream":"ext://sys.stdout"
        },
        "info_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"INFO",
            "formatter":"simple",
            "filename":"info.log",
            "maxBytes":10485760,
            "backupCount":20,
            "encoding":"utf8"
        },
        "error_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"ERROR",
            "formatter":"simple",
            "filename":"errors.log",
            "maxBytes":10485760,
            "backupCount":20,
            "encoding":"utf8"
        }
    },
    "loggers":{
        "my_module":{
            "level":"INFO",
            "handlers":["info_file_handler"],
            "propagate":"no"
        }
    },
    "root":{
        "level":"INFO",
        "handlers":["console","info_file_handler","error_file_handler"]
    }
}
```

### yaml配置文件

```
version: 1
disable_existing_loggers: False
formatters:
        simple:
            format: "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)d : %(message)s"
handlers:
    console:
            class: logging.StreamHandler
            level: DEBUG
            formatter: simple
            stream: ext://sys.stdout
    info_file_handler:
            class: logging.handlers.RotatingFileHandler
            level: INFO
            formatter: simple
            filename: info.log
            maxBytes: 10485760
            backupCount: 20
            encoding: utf8
    warning_file_handler:
          class: logging.handlers.RotatingFileHandler
          level: WARNING
          formatter: simple
          filename: warning.log
          maxBytes: 10485760
          backupCount: 20
          encoding: utf8
    error_file_handler:
            class: logging.handlers.RotatingFileHandler
            level: ERROR
            formatter: simple
            filename: errors.log
            maxBytes: 10485760
            backupCount: 20
            encoding: utf8
loggers:
        debuger:
                level: DEBUG
                handlers: [console]
                propagate: no
        infoer:
                level: INFO
                handlers: [info_file_handler]
                propagate: no
        warninger:
                level: WARNING
                handlers: [console]
                propagate: no
        errorer:
                level: ERROR
                handlers: [error_file_handler]
                propagate: no

root:
    level: INFO
    handlers: [console,info_file_handler,warning_file_handler,error_file_handler]
```

### 加载配置文件

```
import yaml
import logging.config
import os

from app import settings


def init_logging(config_path=None):

    if config_path and os.path.exists(config_path):

        with open(config_path, "r") as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)

```

### 调用方式

```
if __name__ == "__main__":
	#加载配置文件（项目中初始化一次就行）
    init_logging(os.path.join(settings.BASEDIR,"log_config.yaml"))
	#模块中调用
    mlog = logging.getLogger(os.getenv("LOGLEVEL") or 'debuger')
    mlog.error("error")
    mlog.info('info')
    mlog.warning("warning")
    mlog.info(os.path.join(settings.BASEDIR,"log_config.yaml"))
    mlog.info(os.getenv("LOGLEVEL"))

	#json的配置方式的加载调用
    init_logging(os.path.join(settings.BASEDIR,'log_config.json'))
    jlog = logging.getLogger('my_module')
    jlog.info("*"*50)
    jlog.error("this is json config")
```



# 异步发送邮件模块

```
import os
from threading import Thread
from flask import Flask
from flask_mail import Message, Mail

'''
    Flask实例和Mail实例全部独立于主线程，
    规避了应用程序上下文错乱的问题和循环引用的问题
'''

f_app = Flask('email')

f_app.config.update(
    # 邮箱基础配置
    MAIL_SERVER="smtp.qq.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.getenv("QQEMAIL"),
    MAIL_PASSWORD=os.getenv("QQEMAILALLOWEDPWD"),  # 邮箱授权码
    MAIL_DEFAULT_SENDER=os.getenv("QQEMAIL"),
)

email = Mail(f_app)


# send email asynchronously
# 注意，由于主线程中没有对flask_main插件的Mail对象进行实例化和初始化，所以Message依赖的属性没有初始化，所以无法在主线程中进行实例化
# 解决方法：
#   子线程对Mail进行了实例化和初始化，所以Message在子线程中实例化

def _send_async_mail(app, mess):
    with app.app_context():
        message = Message(mess['subject'])
        if isinstance(mess['to'], list):
            message.recipients = mess['to']
        else:
            message.recipients = [mess['to']]

        if mess['body']:
            message.body = mess['body']

        if mess['html']:
            message.html = mess['html']

        email.send(message)


def send_async_mail(subject, to, body=None, html=None):
    '''
    通过线程实现异步调用发送email
    :param subject: 主题
    :param to: 要发送的对象邮箱
    :param body: 文本消息
    :param html: web页面
    :return: 创建的线程对象
    '''

    message = {
        'subject': subject,
        'to': to,
        'body': body,
        'html': html,
    }

    # 通过线程实现异步调用
    thr = Thread(target=_send_async_mail, args=[f_app, message])
    thr.start()

    return thr

```

# 文件上传模块

#### www/file_upload.html

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>upload</title>
</head>
<body>
<div>
    <h1>上传文件</h1>
    <form action="/upload/" enctype="multipart/form-data" method="post">
        <input type="file" name="fileUpload">
        <br>
        <input type="submit" value="submit">
    </form>
</div>
</body>
</html>
```

#### views/upload.py

```
import os
from flask import request, render_template, Blueprint
from werkzeug.utils import secure_filename

bp = Blueprint("upload", __name__)

@bp.route('/upload/',methods=["GET","POST"])
def upload_file():
    method = request.method

    if method == "GET":
        return render_template("file_upload.html")

    elif method == "POST":

        file = request.files['fileUpload']

        file_path = os.path.join('/tmp', 'flask_demo')

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file_path = os.path.join(file_path,secure_filename(file.filename))

        file.save(file_path)

        return render_template("file_upload.html")
    else:
        print("不支持%s请求方法\n" % method)


```



# celery模块

## 配置

utils/tasks/celery_config.py

```
from datetime import timedelta


class Basic_Celery_Conf:
    BROKER_URL = 'redis://127.0.0.1:6379/10'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/11'



class Simple_Celery_Conf(Basic_Celery_Conf):
    CELERY_CONCURRENCY = 2


class Timer_Celery_Conf(Basic_Celery_Conf):

    TIME_ZONE = "Asia/Shanghai"
    CELERYBEAT_SCHEDULE = {
        'say_good_task':{
            'task':'say_good',
            "schedule": timedelta(seconds=10),
        }
    }

```

## 异步任务

### 异步发送邮件

utils/tasks/tasks_v1.py

```
from celery import Celery

from utils.email import send_mail
from utils.tasks.celery_config import *

app = Celery(__name__,config_source=Simple_Celery_Conf)

@app.task
def add(a,b):
    print(a+b)

@app.task
def send_mail_task(subject,to,body=None,html=None):
    send_mail(subject,to,body,html)
```

### email模块

utils/email.py

```
import os
from threading import Thread
from flask import Flask
from flask_mail import Message, Mail

'''
    Flask实例和Mail实例全部独立于主线程，
    规避了应用程序上下文错乱的问题和循环引用的问题
'''

f_app = Flask('email')

f_app.config.update(
    # 邮箱基础配置
    MAIL_SERVER="smtp.qq.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.getenv("QQEMAIL"),
    MAIL_PASSWORD=os.getenv("QQEMAILALLOWEDPWD"),  # 邮箱授权码
    MAIL_DEFAULT_SENDER=os.getenv("QQEMAIL"),
)

email = Mail(f_app)


# send email asynchronously
# 注意，由于主线程中没有对flask_main插件的Mail对象进行实例化和初始化，所以Message依赖的属性没有初始化，所以无法在主线程中进行实例化
# 解决方法：
#   子线程对Mail进行了实例化和初始化，所以Message在子线程中实例化

def _send_async_mail(app, mess):
    with app.app_context():
        message = Message(mess['subject'])
        if isinstance(mess['to'], list):
            message.recipients = mess['to']
        else:
            message.recipients = [mess['to']]

        if mess['body']:
            message.body = mess['body']

        if mess['html']:
            message.html = mess['html']

        email.send(message)


def send_async_mail(subject, to, body=None, html=None):
    '''
    通过线程实现异步调用发送email
    :param subject: 主题
    :param to: 要发送的对象邮箱
    :param body: 文本消息
    :param html: web页面
    :return: 创建的线程对象
    '''

    message = {
        'subject': subject,
        'to': to,
        'body': body,
        'html': html,
    }

    # 通过线程实现异步调用
    thr = Thread(target=_send_async_mail, args=[f_app, message])
    thr.start()

    return thr

def send_mail(subject, to, body=None, html=None):

    message = {
        'subject': subject,
        'to': to,
        'body': body,
        'html': html,
    }

    _send_async_mail(f_app,message)
```

### views中的调用

app/views/celery_view.py

```
from flask import Blueprint

from utils.tasks.tasks_v1 import  send_mail_task

blue = Blueprint('celery_bp',__name__)

@blue.route("/tasks/v1/mail",methods=["GET","POST"])
def send_async_mail():
    send_mail_task.delay(subject="hello",to='fxujunfeng@foxmail.com',body="OK")

    return "OK"
```

### 启用示例

```
 celery -A utils.tasks.tasks_v1 worker -l info
 python manage.py runserver -h 0.0.0.0 -p 5000 -d -r 
```



## 定时任务

### task模块

utils/tasks/tasks_v2.py

```

from celery import Celery

from utils.tasks.celery_config import *

app = Celery(__name__,config_source=Timer_Celery_Conf)

@app.task(name="say_good")
def say_good_v2():
    print("good!")

```

### 启用示例

```
 celery -A utils.tasks.tasks_v2 worker -l info
 celery -A utils.tasks.tasks_v2 beat -l info
```



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

# end



















































