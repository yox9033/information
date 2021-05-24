import redis


class Config(object):
    """配置文件"""
    SECRET_KEY = 'AHSHSHSUS1SDSDS '
    # MYSQL连接配置,禁止追踪数据库修改
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/information'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # redis连接配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    # session配置,指定session存储的数据库类型
    SESSION_TYPE = 'redis'
    # 设置session存储对象,保存session
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 开启session数据的签名
    SESSION_USE_SIGNER = True
    # 设置session有效期
    SESSION_PERMANENT = 3600 * 31


class DevelopConfig(Config):
    """开发环境配置"""
    DEBUG = True


class ProductionConfig(Config):
    """"生产环境配置"""
    DEBUG = False


config_map = {
    "develop": DevelopConfig,
    "production": ProductionConfig
}
