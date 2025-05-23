from model.models import User as modelsUser
from model.models import db


#数据库账号信息
class User():
    def find_user(data):
        Result = modelsUser.query.filter_by(username=data['username']).first()
        return Result

    #注册增加账号信息
    def add_user(data):
        db.session.add(data)
        db.session.commit()
        return {'添加成功'}
