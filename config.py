import redis


class Config(object):
    SECRET_KEY = 'AHSHSHSUS1SDSDS '
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/information'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    SESSION_PERMANENT = 3600 * 31


class DevelopConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_map = {
    "develop": DevelopConfig,
    "production": ProductionConfig
}
