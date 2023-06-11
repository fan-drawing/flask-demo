Flask 框架笔记

# 一、构建框架

## 1、安装 pip3 install flask

## 2、构建

  新建 flask 文件夹 创建 app.py
  写入文件：

  from markupsafe import escape
  from flask import Flask

  app = Flask(__name__)

  @app.route("/")
  def hello_world():
      return "<p>Hello, World!</p>"

  @app.route("/<name>")
  def hello(name):
      return f"Hello world1, {escape(name)}!"

## 3、模板和静态文件

  static 静态文件

  templates 模板文件

## 4、启动框架

  flask run : 一般启动
  flask run --debugger --reload : 开发模式+热更新
  flask run --host=0.0.0.0 : 公网外发

  注意* 模板发生改变时需要重启项目 

# 二、flask基础知识点

  ## 路由设置

  ### flask路由实用route()装饰器来把函数绑定到URL上
  escape html 转义
  
  #### 返回一个html
  @app.route("/")
  def main():
    return f'hello wrold {escape('<script>alert(1)</script>')}'

  使用 redirect() 函数可以重定向。
  使用 abort() 可以 更早退出请求，并返回错码。
  return redirect(url_for('login'))
  abort(401)
  建议不用

  #### 返回json
    import json
    ...
    return response, 200, {"Content-Type": "application/json"}
    return response, 401, {"Content-Type": "application/json"}

  ### 带参数

  带参数
  @app.route('/user/<username>')
  def show_user_profile(username):
      # show the user profile for that user
      return f'User {escape(username)}'
  
  缺省值 string(非/字符串) int float path uuid
  @app.route('/post/<int:post_id>')
  def show_post(post_id):
      # show the post with the given id, the id is an integer
      return f'Post {post_id}'

  @app.route('/path/<path:subpath>')
  def show_subpath(subpath):
      # show the subpath after /path/
      return f'Subpath {escape(subpath)}'

  
  ## 渲染模板

  ### 模板引用
  @app.route("/<name>")
  def hello(name):
    return render_template('index.html', name = name)
  
  /templates/index.html

  ### 静态资源
  <link rel="stylesheet" href="{{ url_for('static', filename='css/index.css') }}">

  ### 赋值

  <span>{{name}}</span>

  ### 条件判断
  {% if name %}
    <h1>Hello {{name}}</h1>
  {% else %}
    <h1>Hello World!</h1>
  {% endif %}

  ### for 循环

  变量	           描述
  loop.index	    当前循环迭代的次数（从 1 开始）
  loop.index0	    当前循环迭代的次数（从 0 开始）
  loop.revindex	  到循环结束需要迭代的次数（从 1 开始）
  loop.revindex0	到循环结束需要迭代的次数（从 0 开始）
  loop.first	    如果是第一次迭代，为 True
  loop.last	      如果是最后一次迭代，为 True
  loop.length	    序列中的项目数
  loop.cycle	    在一串序列间期取值的辅助函数

  {% for api in apis %}
    <div class="btn btn__primary" onclick="postData('{{api.url}}')"><p>{{ api.name }}</p></div>
  {% endfor %}


  ## cookie 设置
    
  看代码
    def set_cookie(
        self,
        key: str,
        value: str = "",
        max_age: t.Optional[t.Union[timedelta, int]] = None,
        expires: t.Optional[t.Union[str, datetime, int, float]] = None,
        path: t.Optional[str] = "/",
        domain: t.Optional[str] = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: t.Optional[str] = None,
    ) -> None:
        """Sets a cookie.

        A warning is raised if the size of the cookie header exceeds
        :attr:`max_cookie_size`, but the header will still be set.

        :param key: the key (name) of the cookie to be set.
        :param value: the value of the cookie.
        :param max_age: should be a number of seconds, or `None` (default) if
                        the cookie should last only as long as the client's
                        browser session.
        :param expires: should be a `datetime` object or UNIX timestamp.
        :param path: limits the cookie to a given path, per default it will
                     span the whole domain.
        :param domain: if you want to set a cross-domain cookie.  For example,
                       ``domain=".example.com"`` will set a cookie that is
                       readable by the domain ``www.example.com``,
                       ``foo.example.com`` etc.  Otherwise, a cookie will only
                       be readable by the domain that set it.
        :param secure: If ``True``, the cookie will only be available
            via HTTPS.
        :param httponly: Disallow JavaScript access to the cookie.
        :param samesite: Limit the scope of the cookie to only be
            attached to requests that are "same-site".
        """

  ## session设置

  除了请求对象之外还有一种称为 session 的对象，允许您在不同请求 之间储存信息。这个对象相当于用密钥签名加密的 cookie ，即用户可以查看您的 cookie ，但是如果没有密钥就无法修改它。


  ## token 认证

  我们先使用 flask_jwt_extended 组件

  pip install flask_jwt_extended

  用到的方法和api：

  JWTManager
  
    class JWTManager(
      app: Flask | None = None,
      add_context_processor: bool = False 
      #上下文处理器模板渲染中是否可访问变量
    )

  create_access_token

    (function) def create_access_token(
      identity: Any,
      # 标识
      fresh: Fresh = False,
      # 是否需要 fresh_token
      expires_delta: ExpiresDelta | None = None,
      # 过期时间
      additional_claims: Any | None = None,
      # 保存的内容
      additional_headers: Any | None = None
    ) -> str
  get_jwt
  get_jwt_identity
  create_refresh_token

    (function) def create_refresh_token(
      identity: Any,
      expires_delta: ExpiresDelta | None = None,
      additional_claims: Any | None = None,
      additional_headers: Any | None = None
    ) -> str

  verify_jwt_in_request

    (function) def verify_jwt_in_request(
      optional: bool = False,
      fresh: bool = False,
      refresh: bool = False,
      locations: LocationType = None,
      verify_type: bool = True,
      skip_revocation_check: bool = False
    ) -> (Tuple[dict, dict] | None)

  jwt_required

  前提配置：
  from datetime import timedelta
  ...
  // 关键
  app.config["JWT_SECRET_KEY"] = "super-secret"
  // 凭证 token 时效 默认 15分钟
  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
  // REFRESH token 时效
  app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)

  我们可采用装饰器的模式使用认证

  from functools import wraps
  ....
  def token_check():
    def wrapper(fn):
      @wraps(fn)
      def decorator(*args, **kwargs):
        // 认证
        verify_jwt_in_request()
        // 获取token中的对应信息
        claims = get_jwt()
        if claims["is_administrator"]:
          return fn(*args, **kwargs)
        else:
          return jsonify(msg="Token check fail!"), 403
      return decorator
    return wrapper
  ...

  // 更新token
  @app.route("/refresh", methods=["POST"])
  @jwt_required(refresh=True) # 刷新token的装饰器，这是最新的写法
  def refresh():
    identity = get_jwt_identity()
    # 只有携带refresh_token才能访问
    access_token = create_access_token(identity=identity,fresh=True)
    if access_token: 
      response = {
        "access_token": access_token
      }
      return response, 200, {"Content-Type": "application/json"}
    else:
      return None, 401, {"Content-Type": "application/json"}

  // 验证token
  @app.route("/protected", methods=["POST"])
  @admin_required()
  def protected():
      return jsonify(foo="bar")

  // 获取token 下面只是为了案例正常代码请不要这么写
  @app.route("/login", methods=['POST', 'GET'])
  def login():
    if request.method == 'POST':
      data = {
        "name": '陈佳兴',
        "age": 22,
        "method": request.method,
        "is_administrator": True,
      }
      // create_access_token 获取token
      // 简单起见这里可以只将用户名作为identity但也可以使用更复杂的设计。
      access_token = create_access_token(
        identity = data['name'],
        additional_claims=data
      )
      // update 字典更新或者添加属性的方法
      data.update({"access_token":access_token})
      // create_refresh_token 生成更新token的凭证
      data.update({"refresh_token":create_refresh_token(identity=data)})
      response = json.dumps(data)
      return response, 200, {"Content-Type": "application/json"}
    else:
      response = json.dumps({
        "code": 401,
        "data": None,
        "errMsg": '接口权限异常'
      })
      return response, 401, {"Content-Type": "application/json"}
  ...
  这就是简单用法当然你可以进一步对权限进行相应的封装,具体使用可以看代码



# 数据库连接及使用

  ## 学习案例使用 sqlite3 数据库

  请先安装 pip3 install pysqlite3

  flask init-db 初始数据库 创建对应的文件（无文件情况下）


  ### 前提条件我们要了解 flask 的上下文
  
  from flask import current_app, g

  #### current_app : current_app是线程、协程隔离对象
    
    AppContext、RequestContext、Flask与Request之间的关系
    AppContext
    应用上下文，是对flask一切对象的封装

    RequestContext
    请求上下文，是对request请求对象的封装
    current_app
    类型是LocalProxy
    像全局变量一样工作，但只能在处理请求期间且在处理它的线程中访问
    返回的栈顶元素不是应用上下文，而是flask的应用实例对象

    应用上下文的封装=flask核心对象+和外部协作对象（再flask封装对象上再添加push、pop等）（请求上下文同理）
  #### g 对象
  

  // 等待上下文存在时
  with app.app_context():
    // 写入配置参数
    current_app.config['SQLLITE_NAME'] = "my-test.db"
    // 初始化数据库配置
    SqlLite.init_sql(app)



  
  ## mysql 安装

  pip3 install pymysql 
  pip3 install flask-sqlalchemy 

  ORM模型和表的映射

# Flask蓝图美化文件层级划分

  from flask import Blueprint

  Blueprint 就是蓝图

  ## 创建拓展文件

  具体使用 添加一个 extend.py 文件
   
  ```extend.py 被Python解释器执行时（脚本），__name__ 这个变量的值就是 "__main__"，如果这个 extend.py 是被 import 到别的文件中执行的话（库），此时的 __name__ 的值就为该导入的库包的文件名extend，那当然不等于 "__main__"```

  from flask import Blueprint,render_template
  extend = Blueprint('extend', __name__)
  @extend.route("/<name>")
  def hello(name):
    # return f"hello wrold {escape(name)}"
    return render_template('demo.html', name = name)

  ## 注入拓展文件

  from extend import extend
  app.register_blueprint(extend)



# 依赖包导出
pip3 install pipreqs
pipreqs ./ 或者 pipreqs ./ --encoding=utf-8

# 依赖包导入
pip3 install -r requirements.txt