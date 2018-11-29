from flask import Blueprint

from utils.email import send_async_mail

blue = Blueprint('mailbp',__name__)

@blue.route("/email/")
def sendmail():
    subject = "Hello"
    to_addr = 'fxujunfeng@foxmail.com'
    body = "Hello Flask"
    html = "<h1>This is a mail test!<h1>"

    send_async_mail(subject,to_addr,body,html)

    return 'ok'
