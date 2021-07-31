
from flask_sqlalchemy import SQLAlchemy
from conf import conf

db = SQLAlchemy()

db_connect_string = f"mysql+pymysql://{conf.get('MYSQL_USER')}:{conf.get('MYSQL_PASS')}@{conf.get('MYSQL_HOST')}:{conf.get('MYSQL_PORT')}/{conf.get('MYSQL_DB')}"
