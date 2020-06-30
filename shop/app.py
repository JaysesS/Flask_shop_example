from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_nav import Nav
from nav import init_custom_nav_renderer, anon, auth

app = Flask(__name__)
app.config.from_pyfile("config.py")

Bootstrap(app)
nav = Nav(app)
nav.register_element('navbarAnon', anon)
nav.register_element('navbarAuth', auth)

init_custom_nav_renderer(app)

db = SQLAlchemy(app)

from views import *

if __name__ == '__main__':
    app.run()