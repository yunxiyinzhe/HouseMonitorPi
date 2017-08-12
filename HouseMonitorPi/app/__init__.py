from flask import Flask
from flask_flatpages import FlatPages

flatpages = []

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    global flatpages
    flatpages = FlatPages(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app

