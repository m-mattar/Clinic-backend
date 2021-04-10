from flask import request, jsonify, abort

from app import app, db, bcrypt
from models.User import User, UserSchema
from api.Auth import create_token, extract_auth_token, decode_token

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


@app.route('/user', methods=['PATCH'])
def update_user():
    # check if user is logged in
    token = extract_auth_token(request)
    if token is None:
        abort(401)

    # check if the updates are allowed
    allowed_updates = {"user_name", "password"}
    for update in request.args.keys():
        if update not in allowed_updates:
            abort(403)

    # update the user
    try:
        user_id = decode_token(token)
        user = User.query.filter_by(id=user_id).first()

        # TODO: this is not updating the user, recheck
        for update in request.args:
            print(update)
            user[update] = request[update]

        db.session.commit()

    except:
        abort(500)

    return jsonify("User updated")


@app.route('/user', methods=['DELETE'])
def delete_user():
    return
