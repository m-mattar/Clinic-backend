from flask import request, jsonify

from app import app, db
from models.User import User, UserSchema

user_schema = UserSchema()


@app.route('/user', methods=['POST'])
def create_user():
    user_name = request.json["user_name"]
    password = request.json["password"]
    is_doctor = request.json["is_doctor"]

    user = User(user_name, password, is_doctor)
    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))
