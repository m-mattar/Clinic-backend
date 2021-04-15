from flask import request, jsonify, abort, Blueprint
from app import db, bcrypt
import jwt
from models.Appointment import Appointment, AppointmentSchema
from api.Auth import extract_auth_token, decode_token
from models.User import User
app_appointment = Blueprint('app_appointment', __name__)
appointments_schema = AppointmentSchema(many=True)
appointment_schema = AppointmentSchema()

@app_appointment.route('/appointment', methods=['POST'])
def book_appointment():
    token=extract_auth_token(request)
    user_id=None
    if(token==None):
        abort(403)
    try:
        user_id=decode_token(token)
    except:
        abort(403)  
    doctor_name = request.json["doctor_name"]
    doctor_id=User.query.filter_by(user_name=doctor_name).first().id
    patient_id = user_id
    appointment_time = request.json["appointment_date"]
    appointment_description = request.json["appointment_description"]
    appo = Appointment(doctor_id, patient_id, appointment_time, appointment_description)
    db.session.add(appo)
    db.session.commit()
    return jsonify(appointment_schema.dump(appo))


@app_appointment.route('/appointment', methods=['PATCH'])
def update_appt():
    # check if user is logged in
    token=extract_auth_token(request)
    user_id=None
    if(token==None):
        abort(403)
    try:
        user_id=decode_token(token)
    except:
        abort(403)  
    # update the user
    appt=request.json['id']
    appt=Appointment.query.filter_by(id=appt).first()
    if(appt.patient_id!=user_id):
        abort(403)
    else:
        appt.appointment_description=request.json["appointment_description"]
        db.session.commit()
    return jsonify(appointment_schema.dump(appt))    



@app_appointment.route('/appointment', methods=['DELETE'])
def delete_appt():
    # check if user is logged in
    token=extract_auth_token(request)
    user_id=None
    if(token==None):
        abort(403)
    try:
        user_id=decode_token(token)
    except:
        abort(403)  
    # update the user
    appt=request.json['id']
    appt=Appointment.query.filter_by(id=appt).first()
    if(appt.patient_id!=user_id):
        abort(403)
    else:
        db.session.delete(appt)
        db.session.commit()
    return jsonify("Appointment Deleted")


@app_appointment.route('/appointment', methods=['GET'])
def get():
    token=extract_auth_token(request)
    user_id=None
    if(token==None):
        abort(403)
    try:
        user_id=decode_token(token)
    except:
        abort(403) 
    #patient=User.query.filter_by(user_name=request['user_name']).first().id
    print(user_id)
    ar=Appointment.query.filter_by(patient_id=user_id).all()
    print(ar)
    ret=jsonify(appointments_schema.dump(ar))
    return ret
        
    
