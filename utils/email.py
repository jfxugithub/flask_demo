from threading import Thread
from flask import  Flask
from flask_mail import Message, Mail

'''
    Flask实例和Mail实例全部独立于主线程，
    规避了应用程序上下文错乱的问题和循环引用的问题
'''

f_app = Flask('mail')
f_app.config.update(
    # 邮箱基础配置
    MAIL_SERVER = "smtp.qq.com",
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'xxxx@qq.com',
    MAIL_PASSWORD = 'xxxx',
    MAIL_DEFAULT_SENDER = 'xxxxx@qq.com'
)

mail = Mail(f_app)

# send email asynchronously
def _send_async_mail(app, message):

    with app.app_context():
        mail.send(message)


def send_async_mail(subject, to,body=None,html=None):

    '''
    通过线程实现异步调用发送email
    :param subject: 主题
    :param to: 要发送的对象邮箱
    :param body: 文本消息
    :param html: web页面
    :return: 创建的线程对象
    '''

    message = Message(subject)
    if isinstance(to, list):
        message.recipients = to
    else:
        message.recipients = [to]

    if body:
        message.body = body

    if html :
        message.html = html

    # 通过线程实现异步调用
    thr = Thread(target=_send_async_mail, args=[f_app, message])
    thr.start()

    return thr

