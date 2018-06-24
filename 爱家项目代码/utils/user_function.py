import os
import redis

from flask import Flask
from flask_session import Session

from aj_user.views import aj_user
from aj_user.house_views import aj_house
from aj_user.order_views import aj_order
from aj_user.models import db

from utils.setting import templates_dir, static_dir

se = Session()


def create_app():
    # 创建app
    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir
                )

    # 创建数据库连接
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:victor@localhost:3306/aj"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 配置redis
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)

    # 注册蓝图
    app.register_blueprint(blueprint=aj_user, url_prefix='/user')
    app.register_blueprint(blueprint=aj_house, url_prefix='/house')
    app.register_blueprint(blueprint=aj_order, url_prefix='/order')

    # 注册数据库模型
    db.init_app(app=app)

    # 注册redis
    se.init_app(app=app)

    return app
