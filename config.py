# default config
class BaseConfig(object):
	DEBUG = False
	SECRET_KEY = 'my precious'

class DevelopmentConfig(BaseConfig):
	DEBUG = False

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
