from flask import Flask

from api.user import user_api
from api.image import image_api
from api.train import train_api
from flask_migrate import Migrate as migrate
import utils.faiss_utils


app=Flask(__name__)
app.register_blueprint(user_api,url_prefix='/user')
app.register_blueprint(image_api,url_prefix='/image')
app.register_blueprint(train_api,url_prefix='/train')

class Config(object):
    #sqlalchemy的配置参数
    SQLALCHEMY_DATABASE_URI = "mysql://root:Db123456789@127.0.0.1:3306/db_pic_faiss"
    #设置每次请求结束后会自动提交数据库的改动，一般设置手动保存
    SQLALCHEMY_COMMIT_ON_TEARDOWN=False
    #设置sqlachemy自动更新跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS=True

#连接数据库
app.config.from_object(Config)
from model.models import db
db.init_app(app)
grate = migrate(app,db)

@app.route('/')
def hello_world():
    return {'message':'Hello,world'}

if __name__ == '__main__':
    app.run('127.0.0.1',8010,debug=True)
