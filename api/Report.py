from app import app


@app.route('/report/test', methods=['GET'])
def create_report():
    return 'youuuppiii!!!!'
