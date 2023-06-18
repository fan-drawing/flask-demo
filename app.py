# from markupsafe import escape
# from werkzeug import secure_filename
import csv
import random
import sqlite3 as sq
import time 
from utils.sets import init_base_sets
from utils.log import init_app_login
import utils.db as SqlLite
from utils.token import init_app_token,check_required
from extend import extend
import urllib
from flask import Response,Flask,flash,render_template,request,make_response,jsonify,current_app,g
import json
from flask_jwt_extended import get_jwt,create_access_token,get_jwt_identity,create_refresh_token,jwt_required
app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# 公共配置文件 
app.config.from_pyfile('./config/config.ini')
print(app.config['UPLOAD_FOLDER'])
init_base_sets(app)
init_app_login(app)

with app.app_context():
  current_app.config['SQLLITE_NAME'] = "./db/my-test.db"
  SqlLite.init_sql(app)
  
jwt = init_app_token(app)

# 蓝图注入
app.register_blueprint(extend, url_prefix = '/extend') # 设置路由前缀 访问 /extend/xxx

def insert_user(username, password):
  sql = "insert into user values (?, ?, ?)"
  conn = g.db
  cursor = conn.cursor()
  try:
    cursor.execute(sql, (None, username, password))
    conn.commit()
  except Exception as e:
    conn.rollback()
    raise TypeError("insert error:{}".format(e)) #抛出异常
  
def query_db(query, args=(), one=False):
    cur= g.db.execute(query, args)
    rv=[dict((cur.description[idx][0], value) for idx,value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.route("/")
def hello_world():
  # 消息闪现
  try:
    insert_user("陈佳兴", "123123")
  except Exception as e:
    app.logger.warning("insert error:{}".format(e))
    flash("insert error:{}".format(e))
  # rows= query_db("select * from user")
  # print(rows)
  resp = make_response(render_template('index.html',apis = [
    {
      'url': '/login',
      'type': 'post',
      'name': '登陆接口 post'
    },
    {
      'url': '/login',
      'type': 'get',
      'name': '登陆接口 get'
    },
    {
      'url': '/protected',
      'type': 'post',
      'name': '验证 post'
    },
    {
      'url': '/refresh',
      'type': 'post',
      'name': '更新 token'
    },
    {
      'url': '/stream',
      'type': 'post',
      'name': '获取数据'
    },
  ]))
  username = request.cookies.get('username')
  if not username:
    resp.set_cookie('username', urllib.parse.quote('陈佳兴'),max_age=24*60*60)
  else:
    print(urllib.parse.unquote(username))
  return resp

@app.route("/protected", methods=["POST"])
@check_required()
def protected():
  rows = query_db("select * from user")
  print(rows)
  return jsonify(foo = "bar", rows = rows)

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True) # 刷新token的装饰器，这是最新的写法
def refresh():
  identity = get_jwt_identity()
  additional_claims = get_jwt()
  access_token = create_access_token(
    identity=identity, 
    additional_claims = additional_claims,
    fresh=True
  )
  if access_token: 
    response = {
      "access_token": access_token
    }
    return response, 200, {"Content-Type": "application/json"}
  else:
    return None, 401, {"Content-Type": "application/json"}

@app.route("/login", methods=['POST', 'GET'])
def login():
  if request.method == 'POST':
    data = {
      "name": '陈佳兴',
      "age": 22,
      "method": request.method,
      "is_administrator": True,
    }
    access_token = create_access_token(
      identity = data['name'],
      additional_claims=data,
      # fresh=True
    )
    data.update({"access_token":access_token})
    data.update({"refresh_token":create_refresh_token(identity = data['name'],additional_claims=data)})
    response = json.dumps(data)
    return response, 200, {"Content-Type": "application/json"}
  else:
    response = json.dumps({
      "code": 401,
      "data": None,
      "errMsg": '接口权限异常'
    })
    return response, 401, {"Content-Type": "application/json"}
  
# @app.route('/nyc_squirrels.csv')
# def generate_large_csv():
#     def generate():
#       for row in iter_all_rows():
#         print(row)
#         yield f"{','.join(row)}\n"
#     return Response(generate(), mimetype = "text/csv")


TEXTS = [
    '你好',
    '这是一段很长很长很长的文本信息，用于演示如何实现流式响应',
    'Hello world',
    'Python是世界上最受欢迎的编程语言之一',
    '天青色等烟雨，而我在等你',
]


@app.route('/stream', methods=['GET','POST'])
def stream():
    def generate():
        long_text = ''
        dunum = 1
        while True:
          dunum+=1
          text = random.choice(TEXTS)
          yield f'{text}\n'
          # print(text, end="", flush=True),
          time.sleep(random.uniform(1, 0.800))  # 随机停顿30~800毫秒后返回下一部分数据
          long_text+=text
          if dunum == 16:
            return long_text
            break
    return Response(generate(), mimetype='text/event-stream')

@app.route('/readStream', methods=['GET','POST'])
def readStream():
    def generate():
      # long_text = '开始'
      with open('./csv/nyc_squirrels.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
          yield f"{'#'+','.join(row)+'#'}\n"
          time.sleep(random.uniform(0.100, 0.200))
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
  app.run(debug = True, port=5000)