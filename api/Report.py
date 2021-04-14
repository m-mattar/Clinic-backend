from flask import Blueprint, jsonify, abort
from models.Report import Report, report_schema
from models.User import User
from Auth import extract_auth_token, decode_token
import jwt

app_report = Blueprint('app_report', __name__)


@app_report.route('/report', methods=['POST'])
def create_report():
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

    report = Report(
        description=request.json['description'],
        appointment_id=request.json['appointment_id']
    )

    db.session.add(report)
    db.session.commit()

    return jsonify(report_schema.dump(report))