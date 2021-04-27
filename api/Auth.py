from flask import request, abort, jsonify, Blueprint
from app import bcrypt
from models.User import User
import datetime
import jwt

SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"

app_auth = Blueprint('app_auth', __name__)


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


@app_auth.route('/authentication', methods=['POST'])
def authentication():
    user_name = request.json["user_name"]
    password = request.json["password"]

    if not user_name or not password:
        abort(400)

    # check if user exists
    user = User.query.filter_by(user_name=user_name).first()
    if user is None:
        abort(404, 'User not found')

    if not bcrypt.check_password_hash(user.hashed_password, password):
        abort(403, 'Incorrect username or password')

    token = create_token(user.id)

    # 0 -> admin
    # 1 -> doctor
    # 2 -> patient
    isDoctor = 2
    if user.is_doctor == 1:
        isDoctor = 1
    elif user.user_name == "admin":
        isDoctor = 0

    return jsonify(
        {
            "token": token,
            "is_doctor": isDoctor
        }
    )


def is_admin_login(req):
    token = extract_auth_token(req)

    user_id = decode_token(token)
    user = User.query.filter_by(id=user_id).first()
    if user is None or user.user_name != "admin":
        return False

    return True
