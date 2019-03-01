import os, sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__, static_url_path='')

DB_URL = os.environ['DB_URL']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
# mysql+pymysql 이어야 한다.
JDBC_CONNECTION_STRING = "mysql+pymysql://%s:%s@%s:3306/%s?charset=utf8" % (DB_USER, DB_PASSWORD, DB_URL, DB_NAME)

app.config['SQLALCHEMY_DATABASE_URI'] = JDBC_CONNECTION_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True         # False for production.

db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def index():
    db.create_all()
    return 'hello zappa!' + JDBC_CONNECTION_STRING


if __name__ == '__main__':
    if len(sys.argv) > 1:
        app.debug = True
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.run(host='0.0.0.0', port=4000)
    else:
        app.run(host='0.0.0.0')
