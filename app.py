from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask import abort
import jwt
import datetime

SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"

# Create app instance
app = Flask(__name__)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)

# Create an instance of SQLAchemy which will act as a reference to our database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:lobster@localhost/exchange'

# Enable access to our backend from other origins (fix to CORS error)
CORS(app)

db = SQLAlchemy(app)

# User class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True)
    hashed_password = db.Column(db.String(128))
    def __init__(self, user_name, password):
        super(User, self).__init__(user_name=user_name)
        self.hashed_password = bcrypt.generate_password_hash(password)

# User Marshmallow schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_name")
        model = User

user_schema = UserSchema()

@app.route("/user", methods=["POST"])
def create_user():
    user = User(
        user_name=request.json["user_name"],
        password=request.json["password"]
    )

    db.session.add(user)
    db.session.commit()

    # return serialized JSON object from our transaction instance.
    return jsonify(user_schema.dump(user))

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

@app.route("/authentication", methods=["POST"])
def authenticate_user():
    # Check if JSON format is valid
    if "user_name" not in request.json or "password" not in request.json:
        abort(400)
    # Check if user exists in database
    user = User.query.filter_by(user_name=request.json["user_name"]).first()
    if user is None:
        abort(403)
    if not bcrypt.check_password_hash(user.hashed_password, request.json["password"]):
        abort(403)

    # Valid credentials, create token and return it as JSON
    return jsonify(token=create_token(user.id))


# Transaction class
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usd_amount = db.Column(db.Float(), nullable=False, unique=False)
    lbp_amount = db.Column(db.Float(), nullable=False, unique=False)
    usd_to_lbp = db.Column(db.Boolean(), nullable=False, unique=False)
    added_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __init__(self, usd_amount, lbp_amount, usd_to_lbp, user_id):
        super(Transaction, self).__init__(usd_amount=usd_amount, lbp_amount=lbp_amount, usd_to_lbp=usd_to_lbp, user_id=user_id, added_date=datetime.datetime.now())

# Transaction Marshmallow schema
class TransactionSchema(ma.Schema):
    class Meta:
        fields = ("id", "usd_amount", "lbp_amount", "usd_to_lbp", "added_date", "user_id")
        model = Transaction

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)

def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get('Authorization')
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None

def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, 'HS256')
    return payload['sub']

@app.route("/transaction", methods=["POST"])
def create_transaction():
    token = extract_auth_token(request)
    user_id = None
    if token is not None:
        try:
            user_id = decode_token(token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            abort(403)

    transaction = Transaction(
        usd_amount=request.json["usd_amount"],
        lbp_amount=request.json["lbp_amount"],
        usd_to_lbp=request.json["usd_to_lbp"],
        user_id=user_id
    )

    db.session.add(transaction)
    db.session.commit()

    # return serialized JSON object from our transaction instance.
    return jsonify(transaction_schema.dump(transaction))

@app.route("/transaction", methods=["GET"])
def get_transactions():
    token = extract_auth_token(request)
    user_id = None
    if token is not None:
        try:
            user_id = decode_token(token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            abort(403)

    transactions = Transaction.query.filter_by(user_id=user_id).all()
    return jsonify(transactions_schema.dump(transactions))

@app.route("/exchangeRate", methods=["GET"])
def getExchangeRate():
    # transactions = Transaction.query.all()
    now = datetime.datetime.now()
    now_minus_3 = now - datetime.timedelta(3)
    transactions = Transaction.query.filter(Transaction.added_date.between(now_minus_3, now)).all()
    usd_to_lbp_rate = 0.0
    usd_to_lbp_count = 0
    lbp_to_usd_rate = 0.0

    for transaction in transactions:
        if transaction.usd_to_lbp:
            usd_to_lbp_rate += transaction.lbp_amount/transaction.usd_amount
            usd_to_lbp_count += 1
        else:
            lbp_to_usd_rate += transaction.usd_amount/transaction.lbp_amount
    
    if usd_to_lbp_count == 0:
        usd_to_lbp_rate = -1
    else:
        usd_to_lbp_rate /= usd_to_lbp_count
    
    if (len(transactions) - usd_to_lbp_count) == 0:
        lbp_to_usd_rate = -1
    else:
        lbp_to_usd_rate /= (len(transactions) - usd_to_lbp_count)

    return jsonify(usd_to_lbp=usd_to_lbp_rate, lbp_to_usd=lbp_to_usd_rate)


