from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()

# Models
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique= False, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    nickname = db.Column(db.String(10), default='')
    email = db.Column(db.String(128), default='')
    user_pic = db.Column(db.String(256), default='')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    records=db.relationship('Record',backref='creator',lazy=True)

class Record(db.Model):
    __tablename__='record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  #这个记录是由id为user.id的用户产生的
    user_image=db.Column(db.String(256), nullable=False) #用户发出的图片
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    images = db.relationship("Image", secondary="record_to_image", backref="records")


#中间表格
class RecordToImage(db.Model):
    __tablename__ = "record_to_image"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_id=db.Column(db.Integer,db.ForeignKey('record.id')) #记录
    image_id = db.Column(db.Integer, db.ForeignKey('image.id')) #图片

class Image(db.Model):
    __tablename__='image'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_name=db.Column(db.String(32), nullable=True)
    image = db.Column(db.String(256), nullable=False, unique=True)  #图片的URL长度不能超过1024
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
