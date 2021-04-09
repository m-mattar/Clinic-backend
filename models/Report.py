from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), nullable=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))

    def __init__(self, description, appointment_id):
        super(Report, self).__init__(description=description, appointment_id=appointment_id)