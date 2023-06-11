import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
 
def init_db():
  db = get_db()
  with current_app.open_resource('schema.sql') as f:
    db.executescript(f.read().decode('utf8'))
 
 
@click.command('init-db')
@with_appcontext
def init_db_command():
  """Clear the existing data and create new tables."""
  init_db()
  click.echo('Initialized the database.')
  
def set_db():
  print('初始化数据库连接')
  if 'db' not in g:
    g.db = sqlite3.connect(
      "my-test.db",
      detect_types=sqlite3.PARSE_DECLTYPES
    )
    g.db.row_factory = sqlite3.Row

def get_db():
  print('初始化数据库连接')
  if 'db' not in g:
    g.db = sqlite3.connect(
      "my-test.db",
      detect_types=sqlite3.PARSE_DECLTYPES
    )
    g.db.row_factory = sqlite3.Row
  return g.db
 
def close_db(e=None):
  db = g.pop('db', None)
  print('数据库关闭')
  if db is not None:
    db.close()


def init_app(app):
  print("初始化数据库配置")
  app.before_request(set_db)
  app.teardown_appcontext(close_db)
  app.cli.add_command(init_db_command)