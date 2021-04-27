from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    CORS(app)

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql@localhost:3306/hospital'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:finally@localhost:3306/hospital'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Arsenal.123@localhost:3306/hospital'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234567qW!@localhost:3306/hospital'
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)

    return app
