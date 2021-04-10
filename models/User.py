from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from app import bcrypt

ma = Marshmallow()
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True)
    hashed_password = db.Column(db.String(128))
    is_doctor = db.Column(db.Boolean, nullable=False)

    def __init__(self, user_name, password, is_doctor):
        super(User, self).__init__(user_name=user_name, is_doctor=is_doctor)
        self.hashed_password = bcrypt.generate_password_hash(password)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_name", "is_doctor")
        model = User


user_schema = UserSchema()
