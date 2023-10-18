from .extensions import db 
from flask_login import UserMixin

#model

class PasswordManager(db.Model):
    __tablename__ = 'PasswordManager'
    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(20), unique=False, nullable=False )
    site_password = db.Column(db.String(20),unique=False,nullable=False)
    site_name = db.Column(db.String(220), nullable=False)

    def __repr__(self):
        return '<PasswordManager %r>' %self.email
    
class User(UserMixin , db.Model):
    id = db.Column(db.Integer , primary_key = True)
    first_name = db.Column(db.String(250))
    last_name = db.Column(db.String(250))
    email = db.Column(db.String(220), nullable = False)
    password = db.Column(db.String(64),nullable = False)

    def __repr__(self):
        return '<User %r>' % self.email

class keymanager(db.Model):
    __bind_key__= 'keymanager'
    id = db.Column(db.Integer, primary_key = True)
    key = db.Column(db.String(250))