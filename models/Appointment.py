from datetime import datetime
from app import db,ma, bcrypt
import random

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(30), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patient_name=db.Column(db.String(30), nullable=False)
    appointment_time = db.Column(db.DateTime)
    appointment_description = db.Column(db.String(300), nullable=True)
    appointment_zoom=db.Column(db.String(300), nullable=True)
    def __init__(self, doctor_name, patient_id, appointment_time, appointment_description, patient_name):
        # assume that it comes like that 
        super(Appointment, self).__init__(doctor_name=doctor_name, patient_id=patient_id,
                                          appointment_description=appointment_description, patient_name=patient_name)
        self.appointment_time = datetime.strptime(appointment_time, '%Y-%m-%dT%H:%M')
        stran=[random.randint(0,10) for i in range(10)]
        self.appointment_zoom="zoom.us/"+doctor_name+"/"+str("".join(map(str,stran)))
class AppointmentSchema(ma.Schema):
    class Meta:
        fields = ("id", "doctor_name", "patient_id", "patient_name", "appointment_time", "appointment_description","appointment_zoom")
        model = Appointment

appointment_scheme=AppointmentSchema()