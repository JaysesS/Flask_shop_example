import os

DEBUG = True
if os.path.isfile("/app/app/database.db"):
    SQLALCHEMY_DATABASE_URI = "sqlite:////app/app/database.db"
elif os.path.isfile("/home/jayse/flask_shop/db/database.db"):
    SQLALCHEMY_DATABASE_URI = "sqlite:////home/jayse/flask_shop/db/database.db"

SECRET_KEY = 'SUPERSECRETKEY'
SQLALCHEMY_TRACK_MODIFICATIONS = False