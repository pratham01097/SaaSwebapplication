from flask_app import db



class User(db.Model):
    __tablename__ = "Login"
    id=db.Column(db.Integer(),primary_key=True)
    username =db.Column(db.String(length=30),unique=True,nullable=False)
    email_address=db.Column(db.String(length=50),unique=True,nullable=False)
    password=db.Column(db.String(length=30),nullable=False)