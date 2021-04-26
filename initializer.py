from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_cors import CORS
from flask import jsonify
from flask_marshmallow import Marshmallow
from flask import abort
import json
from flask_bcrypt import Bcrypt
import datetime
import jwt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Arsenal.123@localhost:3306/hospital'
SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"
ma = Marshmallow(app)
CORS(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt()


# User class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=False)
    Last_name = db.Column(db.String(30), unique=False)
    user_name = db.Column(db.String(30), unique=True)
    hashed_password = db.Column(db.String(128))
    is_doctor = db.Column(db.Boolean, nullable=False)
    information = db.Column(db.String(400), nullable=True, unique=False)

    def __init__(self, user_name, first_name, last_name, information, password):
        super(User, self).__init__(user_name=user_name,
                                   first_name=first_name,
                                   last_name=last_name,
                                   information=information,
                                   is_doctor=False)
        self.hashed_password = bcrypt.generate_password_hash(password)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(30), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    appointment_time = db.Column(db.DateTime)
    appointment_description = db.Column(db.String(300), nullable=True)
    appointment_zoom=db.Column(db.String(300), nullable=True)
    def __init__(self, doctor_name, patient_id, appointment_time, appointment_description):
        # assume that it comes like that 
        super(Appointment, self).__init__(doctor_name=doctor_name, patient_id=patient_id,
                                          appointment_description=appointment_description)
        self.appointment_time = datetime.strptime(appointment_time, '%Y-%m-%dT%H:%M')


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), nullable=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))

    def __init__(self, description, appointment_id):
        super(Report, self).__init__(description=description, appointment_id=appointment_id)

# User Marshmallow schema
