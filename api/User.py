from flask import request, jsonify, abort, Blueprint
from app import db, bcrypt
from models.User import User, UserSchema
from api.Auth import extract_auth_token, decode_token

user_schema = UserSchema()

app_user = Blueprint('app_user', __name__)


def is_admin_login(req):
    token = extract_auth_token(req)

    user_id = decode_token(token)
    user = User.query.filter_by(id=user_id).first()
    if user is None or user.user_name != "admin":
        return False

    return True


@app_user.route('/user', methods=['POST'])
def create_user():
    if not is_admin_login(request):  #comment during dbeugging to cr8 users
        abort(401)

    user_name = request.json["user_name"]
    password = request.json["password"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    information = request.json["information"]
    is_doctor = request.json["is_doctor"]

    user = User(user_name, first_name, last_name, information, is_doctor, password)
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

        user = User.query.filter_by(id=user_id).first()
        user_to_view = User.query.filter_by(user_name=username).first()

        if user_to_view is None:
            abort(404)

        # Admins and Drs can view anyone, normal users cannot
        if not user.user_name == "admin" and not user.is_doctor and not user_to_view.is_doctor:
            abort(401, "You cannot view this profile")

    except Exception as e:
        print(e)
        abort(500)

    return jsonify(user_schema.dump(user))


@app_user.route('/users', methods=['GET'])
def read_all_users():
    if not is_admin_login(request):
        abort(401)

    users = None
    try:
        users = User.query.all()
        if users is None:
            abort(404)

    except Exception as e:
        print(e)
        abort(500)

    user_schema.many = True
    return jsonify(user_schema.dump(users))


@app_user.route('/doctors', methods=['GET'])
def read_doctors():
    doctors = User.query.filter_by(is_doctor=True).all()
    user_schema.many = True
    return jsonify(user_schema.dump(doctors))


@app_user.route('/user/<username>', methods=['PATCH'])
def update_user(username):
    if not is_admin_login(request):
        abort(401)

    # check if the updates are allowed
    allowed_updates = {"user_name", "password", "information", "first_name", "last_name"}
    for update in request.json:
        if update not in allowed_updates:
            abort(400)

    # update the user
    user = None
    try:
        user = User.query.filter_by(id=username).first()

        if user is None:
            abort(404, "User not found")

        for update in request.json:
            if update == "password":
                user.hashed_password = bcrypt.generate_password_hash(request.json[update])
            elif update == "user_name":
                user.user_name = request.json[update]
            elif update == "first_name":
                user.first_name = request.json[update]
            elif update == "last_name":
                user.last_name = request.json[update]
            elif update == "information":
                user.information = request.json[update]
        db.session.commit()

    except Exception as e:
        print(e)
        abort(500, "Could not update profile")

    return jsonify("User updated", user_schema.dump(user))


@app_user.route('/user/<username>', methods=['DELETE'])
def delete_user(username):
    if not is_admin_login(request):
        abort(401)

    try:
        user = User.query.filter_by(id=username).first()

        if user is None:
            abort(404, "User not found")

        db.session.delete(user)
        db.session.commit()

    except Exception as e:
        print(e)
        abort(500, "Not able to delete user")

    return jsonify("User Deleted")
