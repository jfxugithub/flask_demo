from flask import Blueprint

from utils.tasks.tasks_v1 import  send_mail_task

blue = Blueprint('celery_bp',__name__)

@blue.route("/tasks/v1/mail",methods=["GET","POST"])
def send_async_mail():
    send_mail_task.delay(subject="hello",to='fxujunfeng@foxmail.com',body="OK")

    return "OK"

