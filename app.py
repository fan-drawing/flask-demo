from markupsafe import escape
from utils.sets import init_base_sets
from utils.log import init_app_login
from utils.token import init_app_token,check_required
import urllib
from flask import Flask,flash,render_template,request,make_response,jsonify
import json
from flask_jwt_extended import get_jwt,create_access_token,get_jwt_identity,create_refresh_token,jwt_required
app = Flask(__name__)

init_base_sets(app)
init_app_login(app)
jwt = init_app_token(app)

@app.route("/")
def hello_world():
  # 消息闪现
  flash('You were successfully logged in')
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
  ]))
  username = request.cookies.get('username')
  if not username:
    resp.set_cookie('username', urllib.parse.quote('陈佳兴'),max_age=24*60*60)
  else:
    print(urllib.parse.unquote(username))
  app.logger.warning('Watch out!')
  return resp

@app.route("/<name>")
def hello(name):
  # return f"hello wrold {escape(name)}"
  return render_template('base.html', name = name)

# @app.route("/apidemo", methods=["POST"])
# class ApiDemo {
# }


@app.route("/protected", methods=["POST"])
@check_required()
def protected():
  return jsonify(foo="bar")

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True) # 刷新token的装饰器，这是最新的写法
def refresh():
  identity = get_jwt_identity()
  print(identity)
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
if __name__ == '__main__':
  app.run(debug = True, port=5000)