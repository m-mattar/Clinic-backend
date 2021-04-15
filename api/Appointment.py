from flask import request, jsonify, abort, Blueprint
from app import db, bcrypt
import jwt
from models.Appointment import Appointment, AppointmentSchema
from api.Auth import extract_auth_token, decode_token
from models.User import User
app_appointment = Blueprint('app_appointment', __name__)

appointment_schema = AppointmentSchema()

@app_appointment.route('/appointment/test', methods=['GET'])
def book_appointment():
    token=extract_auth_token(request)
    user_id=None
    if(token==None):
        abort(403)
    try:
        user_id=decode_token(token)
    except:
        abort(403)  
    doctor_id = request.json["doctor_id"]
    doctor_id=User.query.filter_by(username=doctor_id).first()
    patient_id = user_id
    appointment_time = request.json["appointment_date"]
    appointment_description = request.json["appointment_description"]
    appo = Appointment(doctor_id, patient_id, appointment_time, appointment_description)
    db.session.add(appo)
    db.session.commit()

    
    
