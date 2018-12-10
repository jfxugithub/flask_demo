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





# modle模型

## modle字段类型

```
 类型名                  Python类型                     说　　明
Integer               int 普通整数                    一般是 32 位
SmallInteger          int 取值范围小的整数             一般是 16 位
BigInteger            int 或 long                    不限制精度的整数
Float                 float                          浮点数
Numeric               decimal.Decimal                定点数
String                str                            变长字符串
Text                  str                            变长字符串，对较长或不限长度的字符串做了优化
Unicode               unicode                        变长 Unicode 字符串
UnicodeText           unicode                        对较长或不限长度的字符串做了优化
Boolean               bool                           布尔值
Date                  datetime.date                  日期
Time                  datetime.time                  时间
DateTime              datetime.datetime              日期和时间
Interval              datetime.timedelta             时间间隔
Enum                  str                            一 组字符串
PickleType            任何 Python 对象                自动使用 Pickle 序列化
LargeBinary           str                            二进制文件

```

## SQLAlchemy约束条件

```
primary_key             如果设为 True，这列就是表的主键
unique                  如果设为 True，这列不允许出现重复的值
index                   如果设为 True，为这列创建索引，提升查询效率
nullable                如果设为 True，这列允许使用空值；如果设为 False，这列不允许使用空值
default                 为这列定义默认值
doc                     字段说明 
```



## modle中的关系

### 一对一关系

```

```

### 一对多关系

models.py--建立关系表

```
from App.ext import db


class Stu(db.Model):
    __tablename__ = 'student'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(30),
        unique=True
    )

	#一对多，外键的声明只能在‘多’中，因为只能外键id只能对应一个：‘一’
    grade_id = db.Column(
        db.ForeignKey('grade.id')
    )

class Grade(db.Model):
    __tablename__ = 'grade'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(30),
        unique=True
    )

	#声明一对多的关系
    stus = db.relationship(
        'Stu',                #对应‘多’的类名
        backref = 'grade',    #为‘多’提供调用属性
        lazy = True           #懒加载
    )


```

views.py

```
from flask import Blueprint

from App.models import *

blue = Blueprint('testbp',__name__)

@blue.route("/get_grade/<int:stu_id>")
def get_grade(stu_id):

    '''
    通过学生id查询班级
    :param stu_id:
    :return:
    '''

    #直接获取外键查询
    # stu = Stu.query.get_or_404(stu_id)
    # grade = Grade.query.get_or_404(stu.grade_id)

    #通过关系查询
    grade = Stu.query.get_or_404(stu_id).grade  #属性grade由Grade表中relationship中的backref决定的
    return grade.name

@blue.route("/get_stu/<int:grade_id>")
def get_stu(grade_id):
    '''
    通过班级查学生
    :param grade_id:
    :return:
    '''
    #直接查询stu表
    # stus = Stu.query.filter(Stu.grade_id == grade_id)

    #根据表关系查询
    stus = Grade.query.get_or_404(grade_id).stus

    stus_name = ''
    for i in stus:
        stus_name += i.name + ";"

    return stus_name
```



### 多对多关系

models.py

```
from App.ext import db


class Tag(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    title = db.Column(
        db.String(20)
    )


tags = db.Table(
    "tags",
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True)
)


class Book(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(20)
    )
    tags = db.relationship(
        "Tag",
        secondary=tags,  # 指定中间表
        backref=db.backref("books", lazy=True),  # 相互的反向引用
        lazy=True
    )
```

views.py

```
@blue.route("/create")
def create_date():
    tag1 = Tag(title="python")
    tag2 = Tag(title="java")


    db.session.add_all([tag1,tag2])
    db.session.commit()

    book1 = Book(name="python黑客功防")
    book1.tags = [tag1,tag2]
    book2 = Book(name='java放弃之道')
    book2.tags = [tag1, tag2]

    db.session.add_all([book1, book2])
    db.session.commit()

    return 'ok'



@blue.route("/get_book/<int:id>")
def get_book(id):
    books = Tag.query.get(id).books
    for i in books:
        print(i.name)

    return "book"

@blue.route("/get_tag/<int:id>")
def get_tag(id):
    tags = Book.query.get(id).tags
    for i in tags:
        print(i.title)

    return 'tag'
```



## modle的特殊熟悉--元信息

```
__tablename__:

        指定数据库中生成的表名

__abstract__:

        在父类中设置为True,则继承该父类的class会单独生成一张表
        默认是所有的子类的属性都会在父类的表中,子类不单独生成一张表

```

# ORM

## 1.插件

​    Flask-SQLAchemy

### 1.1安装插件

​    pip install  Flask-SQLAchemy

### 1.2初始化插件

```
db = SQLAlchemy()

# Flask-SQLAlchemy插件
def init_db(app):
    db.init_app(app)
    
```

## 数据库操作

### 创建数据库

​    db.create_all(object)
    

### 删除库

​    db.drop_all(object)
    

### 添加数据

​    db.session.add(obj)  #添加一条
    db.session.add_all(list[obj])#批量添加

### 删除数据

​    db.session.delete(obj)
    

### 提交数据

​    db.session.commit()
    

### 查询数据

​    object.query.all()  #获取表中的全部数据

#### filter()

​	filter(类名.属性名.运算符(‘xxx’))

​	filter(类名.属性 数学运算符  值)

#### 在filter中可以使用的运算符

```
contains       --包含...
startswith
endswith
in_
like
__gt__
__ge__
__lt__
__le__
and_(a>b,a<d)
or_(a>b,a<d)
not_(a == b)
```

eg：

```
	# id大于20的数据
    dogs = Dog.query.filter(Dog.id.__gt__(20))

    # name等于泰迪9 的数据 使用双等于号
    dogs = Dog.query.filter(Dog.name=="泰迪9")

    # 获取名字包含 34 的数据
    dogs = Dog.query.filter(Dog.name.contains('34'))

    # 获取id 是 9 10 11 数据
    dogs = Dog.query.filter(Dog.id.in_([9, 10, 11]))

    # 获取name以4结尾的数据
    dogs = Dog.query.filter(Dog.name.like("%4_"))
```



#### filter_by()

​    通常用在级联上
    object.query.filter_by()

#### offset()

​    设置偏移量
    object.query.offet(number)

#### limit()

​    获取前number个数据
    object.query.limit(number)
    实现分页
    object.query.offset(nu).limit(nu+number)

#### slice(start,end)

​    实现分页
    object.query.slice(nu,nu+number)
    等同于:
    object.query.offset(nu).limit(nu+number)

#### paginate()

​    实现分页
        page--第几页
        per_page -- 每页显示多少数据
        error_out --  当分页查询出现异常的时候 是否抛出错误 默认抛出 改为Flase
    

```
pagination = object.query.paginate(page,per_page)
pagination的属性有:
      pagination.pages      #分页后的总页数
                page        #当前页码  
                per_page    #每页显示数据的条数
                prev_num    #返回上一页的页码
                next_num    #返回下一页的页码
                has_prev    #是否存在上一页
                has_next    #是否存在下一页 
                
                items       #返回当前页的数据(返回的类型为list,list中保存的是object类的实例)
                iter_pages
pagination对象的方法:
        pagination.iter_pages()  #页码的generator
                  .prev()        #返回上一页的对象
                  .next()        #返回下一页的对象
```

#### order_by()

​    升序排序
    object.query.order_by("s_age").offset(nu).limit(nu+number)
    降序排序
    object.query.order_by("-s_age").offset(nu).limit(nu+number)

#### get()

​    	根据主键获取数据

​	object.query.get(15)

​	如果没有找到想返回404

​	object.query.get_or_404(id)

#### first()

​    获取第一个数据
    object.query.all().first()

​    object.query.all().first_or_404()

# Flask-Migrate

## 1.安装

pip install Flask-Migrate

## 2.懒加载初始化

migrater = Migrate()

migrater.int_app(db,app)

## 3.manage.py中添加

manager.add_command('db',MigrateCommand)

## 4.数据迁移命令

```
$ python manager.py db init   ##初始化，并在根目录下添加migrations文件夹（保存数据库变更的记录） 

$ python manager.py db migrate  ##生成迁移文件

$ python manager.py db upgrade  ##执行迁移修改

$ python manager.py db downgrade  ##回退修改

```

# json

## web中形成json串

```
//json对象转换成json字符串
JSON.stringify({"data": dataArr})  #json官方的转换方式
或
$.parseJSON({"data": dataArr});
```

## web中解析json数据

```angular2html
//由JSON字符串转换为JSON对象
    var obj = eval('(' + jsonstr + ')');  #这种方式不安全eval会执行json串中的表达式
或
    var obj = jsonstr.parseJSON();   
或
    var obj = JSON.parse(jsonstr); #json官方的转换方式
```

## Python中生成json字符串

```angular2html
json.dumps({'a': 1, 'b':1}
或
jsonify({'a': 1, 'b': 2})
```

### json.dumps和 jsonify的区别:

```angular2html
    使用jsonify时响应的Content-Type字段值为application/json，
    而使用json.dumps时该字段值为text/html。
    Content-Type决定了接收数据的一方如何看待数据，如何处理数据，
    如果是application/json，则可以直接当做json对象处理，
    若是text/html，则还要将文本对象转化为json对象再做处理
```

## Python中解析json

```angular2html
json.loads(jsonstr)
```



#  end