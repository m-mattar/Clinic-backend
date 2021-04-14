from app import db
from app import ma


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), nullable=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))

    def __init__(self, description, appointment_id):
        super(Report, self).__init__(description=description, appointment_id=appointment_id)

class ReportSchema(ma.schema):
    class Meta:
        fields = ("id", "description", "appointment_id")
        model = Report

report_schema = ReportSchema()