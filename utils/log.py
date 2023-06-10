import logging
from datetime import timedelta

def init_app_login(app):
  app.config["JWT_SECRET_KEY"] = "super-secret"
  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
  app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
  handler = logging.FileHandler('flask.log', encoding='UTF-8')
  handler.setLevel(logging.DEBUG)
  logging_format = logging.Formatter('%(asctime)s - %(levelname)s - file_name:%(filename)s - function:%(funcName)s - lines:%(lineno)s - message:%(message)s')
  handler.setFormatter(logging_format)
  app.logger.addHandler(handler)