from flask import Flask
from flask_session import Session
import os
import redis
from AdminOs.views import admin_blueprint
from AdminOs.models import db


def create_app():
    # 获取项目根目录路径
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # 拼接static
    static = os.path.join(BASE_DIR, 'static')

    # 拼接templates
    templates = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__,
                static_folder=static,
                template_folder=templates
                )

    # 创建数据库连接
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:victor@localhost:3306/flask2"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 配置redis
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)

    # 注册数据模型
    db.init_app(app=app)

    # 注册redis
    Session(app=app)

    # 注册蓝图
    app.register_blueprint(blueprint=admin_blueprint, url_prefix='/admin')

    return app
