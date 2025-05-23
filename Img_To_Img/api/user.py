from flask import Blueprint, jsonify, request
from model.models import User as modelsUser
from mapper.user import User as mapperUser

user_api = Blueprint('user_api', __name__)

@user_api.route('/',methods=['GET'])
def get_user():
    return jsonify({'message':'用户数据'}),200

@user_api.route('/register',methods=['POST'])
def register():
    data=request.args.to_dict() #获取数据库前端

    #print(data);
    if not data:
        return jsonify({'message':'没有输入账号和密码'}),200
    if not data.get('username') or not data.get('password'):
        return jsonify({'message':'填入的数据不完整'}),200
    if mapperUser.find_user(data):
        return jsonify({'message':'用户名已存在'}),200

    user= modelsUser(
        username=data.get('username'),
        nickname=data.get('nickname',''),
        password=data.get('password')
    )

    mapperUser.add_user(user)  #数据库操作
    return jsonify({'message':'User registered successfully'}),200
