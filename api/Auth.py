from flask import request, abort, jsonify
from app import app, bcrypt
from models.User import User
import datetime
import jwt

SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"


def create_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=4),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )


def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get('Authorization')
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None


def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, 'HS256')
    return payload['sub']


@app.route('/authentication', methods=['POST'])
def authentication():
    user_name = request.json["user_name"]
    password = request.json["password"]

    if not user_name or not password:
        abort(400)

    # check if user exists
    user = User.query.filter_by(user_name=user_name).first()
    if user is None:
        abort(403, 'User not found')

    if not bcrypt.check_password_hash(user.hashed_password, password):
        abort(403, 'Incorrect username or password')

    token = create_token(user.id)
    return jsonify(
        {
            "token": token
        }
    )
