from flask import Flask
from config import Config, DevelopConfig, ProductionConfig, config_map
import redis
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_session import Session
import logging
from logging.handlers import RotatingFileHandler

# 设置日志记录等级
logging.basicConfig(level=logging.DEBUG)
# 创建日志记录器.指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler('logs/log', maxBytes=1024 * 1024 * 100, backupCount=10)
# 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为file_log_handler日志记录器设置格式
file_log_handler.setFormatter(formatter)
# 为全局日志对象添加日志记录器
logging.getLogger().addHandler(file_log_handler)

db = SQLAlchemy()
redis_store = None  # type: redis.StrictRedis


def create_app(config_name):
    # 获取配置文件的key
    config_class = config_map.get(config_name)
    app = Flask(__name__)
    # 加载配置文件DevelopementConfig,ProdutionConfig
    app.config.from_object(config_class)
    # 创建redis对象(用来存储验证码,图片验证码和短信验证码)
    # 使redis_store对象变为全局变量
    global redis_store
    # redis数据库存储的值为byte
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT, decode_responses=True)
    # 初始化
    db.init_app(app)
    # 开启CSRF保护
    CSRFProtect(app)
    # 开启session
    Session(app)

    @app.after_request
    def after_request(response):
        """csrf_token校验"""
        csrf_token = generate_csrf()
        response.set_cookie("csrf_token", csrf_token)
        return response

    # 注册自定义过滤器
    from info.utils.common import do_index_class
    app.add_template_filter(do_index_class, "index_class")

    # 首页

    from info.index import index_blue
    app.register_blueprint(index_blue)
    # 登录注册
    from info.passport import passport_bule
    app.register_blueprint(passport_bule)

    return app
