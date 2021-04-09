from app import app


@app.route('/appointment/test', methods=['GET'])
def book_appointment():
    return 'BANZAAAAAIIII!'
