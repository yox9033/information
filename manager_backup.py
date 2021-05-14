from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import redis


class Config(object):
    DEBUG = True
    SECRET_KEY = 'AHSHSHSUS1SDSDS '
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/information'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    SESSION_PERMANENT = 3600 * 31


app = Flask(__name__)
app.config.from_object(Config)
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
db = SQLAlchemy(app)
CSRFProtect(app)
Session(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    return 'view step06'


if __name__ == '__main__':
    manager.run()
