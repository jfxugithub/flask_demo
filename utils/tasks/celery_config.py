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
