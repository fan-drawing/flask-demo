from functools import wraps
from flask import jsonify
from flask_jwt_extended import JWTManager,get_jwt,create_access_token,get_jwt_identity,create_refresh_token,verify_jwt_in_request,jwt_required

def init_app_token(app):
  return JWTManager(app)

def check_required():
  def wrapper(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
      verify_jwt_in_request(verify_type=False)
      claims = get_jwt()
      print(claims)
      if claims["is_administrator"]:
        return fn(*args, **kwargs)
      else:
        return jsonify(msg="Admins only!"), 403
    return decorator
  return wrapper