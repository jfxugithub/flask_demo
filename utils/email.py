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
    MAIL_SERVER = "smtp.qq.com",
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = '2809276444@qq.com',
    MAIL_PASSWORD = 'udfumdkgeqledeja',      #邮箱授码
    MAIL_DEFAULT_SENDER = '2809276444@qq.com',
)

email = Mail(f_app)

# send email asynchronously
#注意，由于主线程中没有对flask_main插件的Mail对象进行实例化和初始化，所以Message依赖的属性没有初始化，所以无法在主线程中进行实例化
#解决方法：
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



def send_async_mail(subject, to,body=None,html=None):

    '''
    通过线程实现异步调用发送email
    :param subject: 主题
    :param to: 要发送的对象邮箱
    :param body: 文本消息
    :param html: web页面
    :return: 创建的线程对象
    '''

    message = {
        'subject':subject,
        'to':to,
        'body':body,
        'html':html,
    }

    # 通过线程实现异步调用
    thr = Thread(target=_send_async_mail, args=[f_app, message])
    thr.start()

    return thr

