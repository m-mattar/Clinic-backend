from datetime import datetime
from app import db,ma, bcrypt


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    appointment_time = db.Column(db.DateTime)
    appointment_description = db.Column(db.String(300), nullable=True)

    def __init__(self, doctor_id, patient_id, appointment_time, appointment_description):
        # assume that it comes like that
        super(Appointment, self).__init__(doctor_id=doctor_id, patient_id=patient_id,
                                          appointment_description=appointment_description)
        self.appointment_time = datetime.strptime(appointment_time, '%Y-%m-%dT%H:%M')
class AppointmentSchema(ma.Schema):
    class Meta:
        fields = ("id", "doctor_id", "patient_id", "appointment_time", "appointment_description")
        model = Appointment

appointment_scheme=AppointmentSchema()