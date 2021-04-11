from flask import Blueprint

app_report = Blueprint('app_report', __name__)


@app_report.route('/report/test', methods=['GET'])
def create_report():
    return 'youuuppiii!!!!'
