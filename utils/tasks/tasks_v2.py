
from celery import Celery

from utils.tasks.celery_config import *

app = Celery(__name__,config_source=Timer_Celery_Conf)

@app.task(name="say_good")
def say_good_v2():
    print("good!")
