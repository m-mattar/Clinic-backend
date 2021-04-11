from flask import Blueprint
from app import db

app_appointment = Blueprint('app_appointment', __name__)


@app_appointment.route('/appointment/test', methods=['GET'])
def book_appointment():
    return 'BANZAAAAAIIII!'
