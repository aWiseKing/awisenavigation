class BaseConfig:
    """ 基础配置 """
    DEBUG = True
    TESTING = False

class ProductionConfig(BaseConfig):
    """ 生产环境 """
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://awisenavition:PfPtLWTzLF77kLG7@localhost:3306/awisenavition'
    # 是否追踪数据库修改，一般不开启, 会影响性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 是否显示底层执行的SQL语句
    SQLALCHEMY_ECHO = True

class DevelopmentConfig(BaseConfig):
    """ 开发环境 """
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:yidaimingjvn2017@localhost:3306/awisenavition'
    # 是否追踪数据库修改，一般不开启, 会影响性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 是否显示底层执行的SQL语句
    SQLALCHEMY_ECHO = True

class TestingConfig(BaseConfig):
    """ 测试环境 """
    DB_SERVER = 'localhost'
    DEBUG = True
    DATABASE_URI = 'sqlite:///:memory:'

configs = {
    "production":ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    "default": DevelopmentConfig
}