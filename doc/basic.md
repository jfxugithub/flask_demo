# 常用对象

## request

```
- request.method	请求方式 
- request.path 		路由中的路径 
- request.args 		get请求参数 get请求参数的包装，args是一个ImmutableMultiDict对象，类字典					  结构对象 数据存储也是key-value 外层是大列表，列表中的元素是元组，元组中左边					 是key，右边是value 
- request.form 		post请求参数 存储结构个args一致 默认是接收post参数 
					还可以接收PUT，PATCH参数 
- request.url 		完整请求地址 
- request.base_url 	去掉GET参数的URL 
- request.remote_addr	请求的客户端地址 
- request.file 		上传的文件 
- request.headers	请求头 
- request.cookie 	请求中的cookie 


ImmutableMultiDict类型： 
	ImmutableMultiDict类似字典的数据结构 与字典的区别，可以存在相同的键 args、form、files都是ImmutableMultiDict的对象 ‘ ImmutableMultiDict数据获取方式 
	dict['uname'] 
	dict.get('uname') 
	# 推荐(在没有数据为空) dict.getlist('uname') # 获取指定key对应的所有值


```

## response

```
- 直接返回字符串
- render_template 	渲染模板，将模板转换成字符串
- make_response 	创建一个响应，是一个真正的Response
- Response()		创建
```

## config

​	flask原生提供current_app, application 一旦启动，就可以通过current_app.config 获取当前application的所有配置。

## g

​   在同一请求上下文中可以视为全局变量

```
from flask import g
```



# cookie,cache和session机制

## cookie

### 机制

​    cookie实际上是一小段文本信息,当客户端请求服务器时,如果服务器需要记录该用户状态,就是用response向浏览器颁发一个cookie,客户端浏览器会把cookie保存起来.
    当浏览器再次向该网站请求时,就会携带cookie下发,服务器就可以通过检验cookie来确认身份.
    

### **特性**:

```
-客户端会话技术<br>

-数据都存储在浏览器中<br>

-支持过期<br>

-不能跨域名<br>

-不能跨浏览器<br>

-cookie是通过response来进行操作的
```

### cookie的使用:

```
1.导入make_response包和request包
from flask import make_response,request

2.创建响应
resp = make_response(render_template("index.html"))
or
resp = redirect(url_for("indexBP.to_index"))

3.设置cookie并返回给浏览器
resp.set_cookie("user",value=username)
return resp

4.获取cookie
request.cookies.get("user")

5.删除cookie

resp.delete_cookie('user')
return resp

```

## session

### 机制

​    是服务器端使用的一种记录客户端状态的机制,数据存放在server端,客户端再次访问的时候只需要从session中找到该客户的状态就可以了.

### **特性:**

1.server端会话技术

2.对数据进行数据安全操作

3.默认在内存中
    

```
-不易管理

-容易丢失

-不能多台电脑协作
```

4.flask-session 默认有效期31天



### session在flask中的配置

```
    #设置会话路徑,即决定哪些路由下应该设置cookies；默认"/",所有路由下都会设置cookie
    SESSION_COOKIE_PATH = '/'
    
    # 使用session的时候必须要添加密钥
    #生成方式:os.urandom(24)
    SECRET_KEY = b'\xbb\x1aSQ\x94O\xa9\xce6\xd4\x19\xf6\xbe\xdb\xc08\xdc\x04\x00\xaf\xa5\x99-\xe1'
    
    #为cookie设置签名来保护数据不被更改
    SESSION_USE_SIGNER = True

    #设置session的存储信息
    # 指明保存到redis中
    SESSION_TYPE = "redis"

    # 定制化将session存储在指定位置
    SESSION_REDIS = redis.StrictRedis(host="127.0.0.1", db=1)

    #设置session的有效期(单位：S)
    PERMANENT_SESSION_LIFETIME = 60 * 3

    #设置session的头
    SESSION_KEY_PREFIX = "test:"
```



### session的使用:

```
1.初始化
from flask_session import Session
sess = Session()
sess.init_app(app)


2.views.py
@blue.route("/set")
def set():
    session['name']='tom'
    return 'ok'

@blue.route('/get')
def get():
    res = session.get('name')
    return res or '过期了'

```



## cache

### 在settings中的配置

```
CACHES = {
    "default": {
        "CACHE_TYPE": "redis", #指定缓存是redis
        "CACHE_REDIS_URL": "redis://127.0.0.1:6379/2"  #redis的URL
    },
    "debug:": {
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_URL": "redis://127.0.0.1:6379/3"
    }
}
```

### cache 的使用

```
1.初始化

from flask_caching import Cache

cache = Cache(config=CACHES.get(os.getenv('CACHE_CONFIG') or 'default'))
cache.init_app(app)


2.views.py
@blue.route("/")
@cache.cached(timeout=60)
def cache_page():
    '''
    页面的缓存
    :return:
    '''
    print(1)
    return 'ok'

@blue.route("/cache")
def cache_num():
    cache.set("name","alan",60)
    return 'ok'


@blue.route("/cache_get")
def cache_get():
    print(2)
    res = cache.get('name') or '缓存已失效'
    return res

```

