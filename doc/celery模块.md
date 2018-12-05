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



# 