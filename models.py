from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db=SQLAlchemy()




class Info(db.Model):
    __tablename__="info"
    title=db.Column(db.String(255),nullable=False)
    content=db.Column(db.String(255),nullable=True)
    time=db.Column(db.String(255),nullable=False)
    source=db.Column(db.String(100),nullable=False)
    href=db.Column(db.String(255),nullable=False,primary_key=True)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin,db.Model):
    __tablename__='user'
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(80), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self,):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


