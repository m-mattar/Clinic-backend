from app import db, ma, bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=False)
    last_name = db.Column(db.String(30), unique=False)
    user_name = db.Column(db.String(30), unique=True)
    hashed_password = db.Column(db.String(128))
    is_doctor = db.Column(db.Boolean, nullable=False)
    information = db.Column(db.String(400), nullable=True, unique=False)

    def __init__(self, user_name, first_name, last_name, information, password):
        super(User, self).__init__(user_name=user_name,
                                   first_name=first_name,
                                   last_name=last_name,
                                   information=information,
                                   is_doctor=False)
        self.hashed_password = bcrypt.generate_password_hash(password)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_name", "first_name", "last_name", "information")
        model = User


user_schema = UserSchema()
