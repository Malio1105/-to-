from flask import Flask

from api.user import user_api
from api.image import image_api
from api.train import train_api
from flask_migrate import Migrate as migrate
from flask_jwt_extended import JWTManager
from mapper.extensions import cache
import config

app=Flask(__name__)
app.register_blueprint(user_api,url_prefix='/user')
app.register_blueprint(image_api,url_prefix='/image')
app.register_blueprint(train_api,url_prefix='/train')

#连接mysql数据库
app.config.from_object(config.MysqlConfig)
from model.models import db
db.init_app(app)
grate = migrate(app,db)

# 配置Redis
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0

# 初始化缓存
cache.init_app(app)

#token配置
app.config['JWT_SECRET_KEY'] = "default-insecure-secret" #配置密钥
app.config["JWT_HEADER_TYPE"] = "" #允许不带类型前缀
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"  # 默认就是Authorization
jwt = JWTManager(app)  # 必须在配置后初始化

@app.route('/')
def hello_world():
    return {'message':'Hello,world'}

if __name__ == '__main__':
    app.run('127.0.0.1',8010,debug=True)
