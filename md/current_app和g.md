
#  请求方法、g对象和钩子函数

## g对象

  - before_request：在每次请求之前执行。通常可以用这个装饰器来给视图函数增加一些变量。

  - teardown_appcontext：不管是否有异常，注册的函数都会在每次请求之后执行。

  - template_filter：在使用Jinja2模板的时候自定义过滤器。比如可以增加一个upper的过滤器（当然Jinja2已经存在这个过滤器，本示例只是为了演示作用）：

  - context_processor：上下文处理器。返回的字典中的键可以在模板上下文中使用。

  - errorhandler：errorhandler接收状态码，可以自定义返回这种状态码的响应的处理方法。

## 额外的讲解: g

  ### Flask中current_app和g对象
  
  请求方法、g对象和钩子函数
 
  #### g对象
  g：global

  g对象是专门用来保存用户的数据的。
  g对象在一次请求中的所有的代码的地方，都是可以使用的。
  使用步骤：

  1.创建一个utils.py文件，用于测试除主文件以外的g对象的使用
    
    utils.py

    #encoding: utf-8

    from flask import g

    def login_log():
        print u'当前登录用户是：%s' % g.username

    def login_ip():
        print u'当前登录用户的IP是：%s' % g.ip

  2.在主文件中调用utils.py中的函数

    #encoding: utf-8

    from flask import Flask,g,request,render_template
    from utils import login_log,login_ip

    app = Flask(__name__)


    @app.route('/')
    def hello_world():
        return 'Hello World!'


    @app.route('/login/',methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        else:
            username = request.form.get('username')
            password = request.form.get('password')
            g.username = username
            g.ip = password
            login_log()
            login_ip()
            return u'恭喜登录成功！'

    if __name__ == '__main__':
        app.run()


  ## 四、钩子函数

     在程序正常运行的时候，程序按照A函数—->B函数的顺序依次运行；钩子函数可以插入到A函数到B函数运行中间从而，程序运行顺序变成了A—->钩子函数—->B函数。

     Flask项目中有两个上下文，一个是应用上下文（app），另外一个是请求上下文（request）。请求上下文request和应用上下文current_app都是一个全局变量。所有请求都共享的。Flask有特殊的机制可以保证每次请求的数据都是隔离的，即A请求所产生的数据不会影响到B请求。所以可以直接导入request对象，也不会被一些脏数据影响了，并且不需要在每个函数中使用request的时候传入request对象。这两个上下文具体的实现方式和原理可以没必要详细了解。只要了解这两个上下文的四个属性就可以了：

    request：请求上下文上的对象。这个对象一般用来保存一些请求的变量。比如method、args、form等。
    session：请求上下文上的对象。这个对象一般用来保存一些会话信息。
    current_app：返回当前的app。
    g：应用上下文上的对象。处理请求时用作临时存储的对象。
    常用的钩子函数
    before_first_request：处理第一次请求之前执行。
    例如以下代码：

      @app.before_first_request
      def first_request():
          print 'first time request'
    before_request：在每次请求之前执行。通常可以用这个装饰器来给视图函数增加一些变量。
    例如以下代码：

      @app.before_request
      def before_request():
          if not hasattr(g,'user'):
              setattr(g,'user','xxxx')

    teardown_appcontext：不管是否有异常，注册的函数都会在每次请求之后执行。

      @app.teardown_appcontext
      def teardown(exc=None):
          if exc is None:
              db.session.commit()
          else:
              db.session.rollback()
              db.session.remove()

    template_filter：在使用Jinja2模板的时候自定义过滤器。比如可以增加一个upper的过滤器（当然Jinja2已经存在这个过滤器，本示例只是为了演示作用）：
    
      @app.template_filter
      def upper_filter(s):
          return s.upper()
    
    context_processor：上下文处理器。返回的字典中的键可以在模板上下文中使用。
    例如：

      @app.context_processor
      def my_context_processor():
          return {'current_user':'xxx'}
    
    errorhandler：errorhandler接收状态码，可以自定义返回这种状态码的响应的处理方法。
    例如：

      @app.errorhandler(404)
      def page_not_found(error):
          return 'This page does not exist',404
    
    额外的讲解: g
    
      g 也是我们常用的几个全局变量之一。在最开始这个变量是挂载在 Request Context 下的。但是在 0.10 以后，g 就是挂载在 App Context 下的。可能有同学不太清楚为什么要这么做。

      首先，说一下 g 用来干什么

      官方在上下文这一张里有这一段说明

      The application context is created and destroyed as necessary. It never moves between threads and it will not be shared between requests. As such it is the perfect place to store database connection information and other things. The internal stack object is called flask.appctx_stack. Extensions are free to store additional information on the topmost level, assuming they pick a sufficiently unique name and should put their information there, instead of on the flask.g object which is reserved for user code.

      大意就是说，数据库配置和其余的重要配置信息，就挂载 App 对象上。但是如果是一些用户代码，比如你不想一层层函数传数据的话，然后有一些变量需要传递，那么可以挂在 g 上。

     同时前面说了，Flask 并不仅仅可以当做一个 Web Framework 使用，同时也可以用于一些非 web 的场合下。在这种情况下，如果 g 是属于 Request Context 的话，那么我们要使用 g 的话，那么就需要手动构建一个请求，这无疑是不合理的。

      g一般用来传递上下文的数据，flask里面有很多钩子函数，例如before_first_request之类的，g提供了一个方法将数据共享到正常的路由函数里去。举个例子，你可以在before_request里面做Http Basic Authentication验证，然后将验证过的用户数据存在g里面，这样在路由函数里就可以直接调用g里面的用户数据了，而不用再搞个全局变量。这样非常方便

  ### Flask中current_app和g对象

      Flask中有两种上下文，请求上下文和应用上下文。

      请求上下文(request context): request和session都属于请求上下文对象。

      request：封装了HTTP请求的内容，针对的是http请求。举例：user = request.args.get('user')，获取的是get请求的参数。

      session：用来记录请求会话中的信息，针对的是用户信息。举例：session['name'] = user.id，可以记录用户信息。还可以通过session.get('name')获取用户信息。

      应用上下文(application context): current_app和g都属于应用上下文对象。

      current_app:表示当前运行程序文件的程序实例。

      g:处理请求时，用于临时存储的对象，每次请求都会重设这个变量。比如：我们可以获取一些临时请求的用户信息。

      当调用app = Flask(_name_)的时候，创建了程序应用对象app；
      request 在每次http请求发生时，WSGI server调用Flask.call()；然后在Flask内部创建的request对象；
      app的生命周期大于request和g，一个app存活期间，可能发生多次http请求，所以就会有多个request和g。
      最终传入视图函数，通过return、redirect或render_template生成response对象，返回给客户端。
      区别： 请求上下文：保存了客户端和服务器交互的数据。 应用上下文：在flask程序运行过程中，保存的一些配置信息，比如程序文件名、数据库的连接、用户信息等。

      上下文对象的作用域
      在flask项目中某一个功能中会有多个视图，那么from flask import request,current_app,session,g，怎么保证某次请求的上下文不会被别的视图拿走呢？

      _request_ctx_stack = LocalStack()
      _app_ctx_stack = LocalStack()
      current_app = LocalProxy(_find_app)
      request = LocalProxy(partial(_lookup_req_object, 'request'))
      session = LocalProxy(partial(_lookup_req_object, 'session'))
      g = LocalProxy(partial(_lookup_app_object, 'g'))

      线程有个叫做ThreadLocal的类，也就是通常实现线程隔离的类。而werkzeug自己实现了它的线程隔离类：werkzeug.local.Local。LocalStack就是用Local实现的。

      LocalStack是flask定义的线程隔离的栈存储对象，分别用来保存应用和请求上下文。
      它是线程隔离的意思就是说，对于不同的线程，它们访问这两个对象看到的结果是不一样的、完全隔离的。这是根据pid的不同实现的，类似于门牌号。

      而每个传给flask对象的请求，都是在不同的线程中处理，而且同一时刻每个线程只处理一个请求。所以对于每个请求来说，它们完全不用担心自己上下文中的数据被别的请求所修改。

      而这个LocalProxy 的作用就是可以根据线程/协程返回对应当前协程/线程的对象，也就是说

      线程 A 往 LocalProxy 中塞入 A

      线程 B 往 LocalProxy 中塞入 B

      无论在是什么地方，

      线程 A 永远取到得是 A，线程 B 取到得永远是 B