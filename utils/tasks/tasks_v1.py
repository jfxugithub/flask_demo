from celery import Celery

from utils.email import send_mail
from utils.tasks.celery_config import *

app = Celery(__name__,config_source=Simple_Celery_Conf)

@app.task
def send_mail_task(subject,to,body=None,html=None):
    send_mail(subject,to,body,html)