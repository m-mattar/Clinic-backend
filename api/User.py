from flask import request, jsonify, abort, Blueprint
from app import db, bcrypt
from models.User import User, UserSchema
from api.Auth import extract_auth_token, decode_token

user_schema = UserSchema()

app_user = Blueprint('app_user', __name__)


@app_user.route('/user', methods=['POST'])
def create_user():
    user_name = request.json["user_name"]
    password = request.json["password"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    information = request.json["information"]

    user = User(user_name, first_name, last_name, information, password)
    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))


@app_user.route('/user', methods=['GET'])
def read_profile():
    token = extract_auth_token(request)
    if token is None:
        abort(401)

    user = None
    try:
        user_id = decode_token(token)
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            abort(404)
    except Exception as e:
        print(e)
        abort(500)

    return jsonify(user_schema.dump(user))


@app_user.route('/user/<username>', methods=['GET'])
def read_user(username):
    token = extract_auth_token(request)
    if token is None:
        abort(401)

    user = None
    try:
        user_id = decode_token(token)
        if user_id is None:
            abort(401, "You are not logged in")

        user = User.query.filter_by(user_name=username).first()
        if user is None:
            abort(404)
        if not user.is_doctor:
            abort(401, "The user you are trying to view is not a doctor")

    except Exception as e:
        print(e)
        abort(500)

    return jsonify(user_schema.dump(user))


# TODO(not returning properly)
@app_user.route('/doctors', methods=['GET'])
def read_doctors():
    token = extract_auth_token(request)
    if token is None:
        abort(401)

    doctors = None
    try:
        user_id = decode_token(token)
        if user_id is None:
            abort(401, "You are not logged in")

        doctors = User.query.filter_by(is_doctor=True).all()
    except Exception as e:
        print(e)
        abort(500)

    print(doctors)
    return jsonify(user_schema.dump(doctors))


@app_user.route('/user', methods=['PATCH'])
def update_user():
    # check if user is logged in
    token = extract_auth_token(request)
    if token is None:
        abort(401)

    # check if the updates are allowed
    allowed_updates = {"user_name", "password"}
    for update in request.json:
        if update not in allowed_updates:
            abort(400)

    # update the user
    user = None
    try:
        user_id = decode_token(token)
        print(user_id)
        user = User.query.filter_by(id=user_id).first()

        for update in request.json:
            if update == "user_name":
                user.user_name = request.json[update]
            elif update == "password":
                user.hashed_password = bcrypt.generate_password_hash(request.json[update])

        db.session.commit()

    except Exception as e:
        print(e)
        abort(500, "Could not update profile")

    return jsonify("User updated", user_schema.dump(user))


@app_user.route('/user', methods=['DELETE'])
def delete_user():
    # check if user is logged in
    token = extract_auth_token(request)
    if token is None:
        abort(401)

    try:
        user_id = decode_token(token)
        print(user_id)
        user = User.query.filter_by(id=user_id).first()

        if user is None:
            abort(404, "User not found")

        print(user.user_name)
        db.session.delete(user)
        db.session.commit()

    except Exception as e:
        print(e)
        abort(500, "Not able to delete user")

    return jsonify("User Deleted")
