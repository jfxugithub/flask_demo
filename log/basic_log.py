import json

import yaml
import logging.config
import os

from app import settings

LOG_PATH = "/tmp/log/"


def init_logging(config_path=None):
    if config_path and os.path.exists(config_path):
        # 判断log的path是否存在，不存在则创建
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)

        file_type = config_path.split('.')[-1]

        if file_type == 'yaml':
            type_load = yaml.load
        elif file_type == 'json':
            type_load = json.load
        else:
            raise ValueError("Not Suport This Type Config File: %s" % config_path)

        with open(config_path, "r") as f:
            config = type_load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    init_logging(os.path.join(settings.BASEDIR, "log_config.yaml"))

    mlog = logging.getLogger(os.getenv("LOGLEVEL") or 'debuger')

    mlog.error("error")
    mlog.info('info')
    mlog.warning("warning")
    mlog.info(os.path.join(settings.BASEDIR, "log_config.yaml"))
    mlog.info(os.getenv("LOGLEVEL"))

    init_logging(os.path.join(settings.BASEDIR, 'log_config.json'))
    jlog = logging.getLogger('my_module')
    jlog.info("*" * 50)
    jlog.error("this is json config")
