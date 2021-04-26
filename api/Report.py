from flask import Blueprint, jsonify, abort, request
from api.Auth import extract_auth_token, decode_token
import jwt
from app import db, bcrypt
from models.Report import Report, report_schema, reports_schema
from models.User import User

app_report = Blueprint('app_report', __name__)


@app_report.route('/reports', methods=['POST'])
def create_report():
    token = extract_auth_token(request)
    user_id = None
    if token is not None:
        try:
            user_id = decode_token(token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            abort(403)

    user = User.query.filter_by(id=user_id).first()

    report = Report(
        description=request.json['description'],
        appointment_id=request.json['appointment_id']
    )

    db.session.add(report)
    db.session.commit()

    return jsonify(report_schema.dump(report))

@app_report.route('/reports', methods=['PATCH'])
def change_report_description():
    token = extract_auth_token(request)
    user_id = None
    if token is not None:
        try:
            user_id = decode_token(token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            abort(403)

    user = User.query.filter_by(id=user_id).first()
    if not user.isDoctor:
        abort(403)

    report = Report.query.filter_by(appointment_id=request.json['appointment_id']).first()
    report.description = request.json['description']

    db.session.commit()

    return jsonify(report_schema.dump(report))

@app_report.route('/reports/AppointmentID', methods=['PATCH'])
def change_report_appointment_id():
    token = extract_auth_token(request)
    user_id = None
    if token is not None:
        try:
            user_id = decode_token(token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            abort(403)

    user = User.query.filter_by(id=user_id).first()
    if not user.isDoctor:
        abort(403)
    
    report = Report.query.filter_by(id=request.json['report_id']).first()
    report.appointment_id = request.json['appointment_id']

    db.session.commit()

    return jsonify(report_schema.dump(report))

@app_report.route('/reports', methods=['DELETE'])
def delete_report():
    token = extract_auth_token(request)
    user_id = None
    if token is not None:
        try:
            user_id = decode_token(token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            abort(403)

    user = User.query.filter_by(id=user_id).first()
    if not user.isDoctor:
        abort(403)

    report = Report.query.filter_by(id=request.json['report_id']).first()
    db.session.delete(report)
    db.session.commit()

@app_report.route('/reports', methods=['GET'])
def all_reports():
    token = extract_auth_token(request)
    user_id = None
    if token is not None:
        try:
            user_id = decode_token(token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            abort(403)

    reports = Report.query.all()
    return jsonify(reports_schema.dump(reports))


@app_report.route('/reports/AppointmentID', methods=['POST'])
def appointment_reports():
    token = extract_auth_token(request)
    user_id = None
    if token is not None:
        try:
            user_id = decode_token(token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            abort(403)

    report = Report.query.filter_by(appointment_id=request.json['appointment_id']).first()
    return jsonify(report_schema.dump(report))