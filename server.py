from app import create_app
from api.User import app_user
from api.Report import app_report
from api.Appointment import app_appointment
from api.Auth import app_auth

app = create_app()

app.register_blueprint(app_user)
app.register_blueprint(app_report)
app.register_blueprint(app_appointment)
app.register_blueprint(app_auth)

