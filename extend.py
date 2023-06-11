from flask import Blueprint,render_template

extend = Blueprint('extend', __name__)

@extend.route("/<name>")
def hello(name):
  # return f"hello wrold {escape(name)}"
  return render_template('demo.html', name = name)