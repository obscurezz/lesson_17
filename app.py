# app.py

from flask import Flask
from namespaces import api

from config import DevelopmentConfig
from models import db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
