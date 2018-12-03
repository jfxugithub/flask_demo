import os
import redis

# 配置 static路径和templates路径,app/__init_中调用

BASEDIR = os.getcwd();

#静态文件路径配置
STATICPATH = os.path.join(BASEDIR, "app/www")

#模板文件路径配置
TEMPLATESPATH = os.path.join(BASEDIR, "app/www/html")

####################################################################
# 配置数据库
DATABASE = {
    "ENGIN": 'mysql',

    "DRIVER": "pymysql",

    "USER": os.getenv("DB_USERNAME"),

    "PASSWORD": os.getenv("DB_PASSWORD"),

    "DOMAIN": "127.0.0.1",

    "PORT": "3306",

    "NAME": "db_demo"
}


def get_database_uri(database):
    '''
    生成链接数据库的URI
    :param database:
    :return: 链接数据库的URI
    '''
    engin = database.get("ENGIN")

    driver = database.get("DRIVER")

    user = database.get("USER")

    password = database.get("PASSWORD")

    domain = database.get("DOMAIN")

    port = database.get("PORT")

    name = database.get("NAME")

    ##数据库名+数据库驱动://username:password@url:port/databaseName
    return "{}+{}://{}:{}@{}:{}/{}".format(engin, driver, user, password, domain, port, name)

###########################################################################################

class BasicConfig:

    DEBUG = False

    # 使用session的时候必须要添加密钥
    #生成方式:os.urandom(24)
    SECRET_KEY = b'\xbb\x1aSQ\x94O\xa9\xce6\xd4\x19\xf6\xbe\xdb\xc08\xdc\x04\x00\xaf\xa5\x99-\xe1'

    #设置session的存储信息
    # 指明保存到redis中
    SESSION_TYPE = "redis"

    CACHE_TYPE = "redis"

class DevelopConfig(BasicConfig):

    DEBUG = True

    #设置会话路徑,即决定哪些路由下应该设置cookies；默认"/",所有路由下都会设置cookie
    SESSION_COOKIE_PATH = '/'

    # 定制化将session存储在指定位置
    SESSION_REDIS = redis.StrictRedis(host="127.0.0.1", db=1)

    #设置session的有效期(单位：S)
    PERMANENT_SESSION_LIFETIME = 60 * 3

    #设置session头
    SESSION_KEY_PREFIX = "demo:"

    # SQLAlchemy配置
    SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 邮箱配置
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '2809276444@qq.com'
    MAIL_PASSWORD = 'udfumdkgeqledeja'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME


# 加载配置环境,目前就设置了开发环境配置
ENV = {
    "default": DevelopConfig,

    "development": DevelopConfig,

    "test": DevelopConfig,

    "product":DevelopConfig
}

CACHES = {
    "default": {
        "CACHE_TYPE": "redis", #指定缓存存储：redis
        "CACHE_REDIS_URL": "redis://127.0.0.1:6379/2"
    },
    "debug:": {
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_URL": "redis://127.0.0.1:6379/3"
    }
}



