from model.models import User as modelsUser
from model.models import db


#数据库账号信息
class User():
    def findByusername(username):
        Result = modelsUser.query.filter_by(username=username).first()
        return Result

    def findByemail(email):
        Result = modelsUser.query.filter_by(email=email).first()
        return Result

    #注册增加账号信息
    def add_user(data):
        db.session.add(data)
        db.session.commit()
        return {'添加成功'}
