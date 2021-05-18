from flask import Flask
from config import Config,DevelopConfig,ProductionConfig,config_map
import redis
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session

db = SQLAlchemy()
def create_app(config_name):
    config_class = config_map.get(config_name)
    app = Flask(__name__)
    app.config.from_object(config_class)
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)
    db.init_app(app)
    CSRFProtect(app)
    Session(app)


    from info.index import index_blue
    app.register_blueprint(index_blue)
    return app

