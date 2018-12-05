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



# 