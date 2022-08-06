import os


class DevelopmentConfig(object):
    DEBUG = True
    SECRET_KEY = os.urandom(12)
    RESTX_JSON = {'ensure_ascii': False}
    JSON_SORT_KEYS = False
    JSON_AS_ASCII = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


class PaginationConfig(object):
    PAGE = 1
    PER_PAGE = 3
