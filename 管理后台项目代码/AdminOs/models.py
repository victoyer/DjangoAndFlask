from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# 用户信息
class User(db.Model):
    u_id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 主键
    u_name = db.Column(db.String(16), unique=True)  # 用户名
    u_pwd = db.Column(db.String(200))  # 用户密码
    u_data = db.Column(db.DateTime, default=datetime.now)  # 用户注册时间
    roles = db.Column(db.Integer, db.ForeignKey('roles.r_id'), nullable=True)  # 关联角色表
    is_Delete = db.Column(db.Boolean, default=False)  # 逻辑删除

    __tablename__ = 'user'

    # 初始化用户实例
    def __init__(self, name, pwd, r_id):
        self.u_name = name
        self.u_pwd = pwd
        self.roles = r_id

    # 保存创建的用户实例
    def save(self):
        db.session.add(self)
        db.session.commit()


# 学生信息
class Student(db.Model):
    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 主键
    s_name = db.Column(db.String(16))  # 学生姓名
    s_age = db.Column(db.Integer)  # 学生年龄
    s_sex = db.Column(db.Boolean)  # 学生性别
    is_Delete = db.Column(db.Boolean, default=False)  # 逻辑删除
    grade = db.Column(db.Integer, db.ForeignKey('grade.g_id'), nullable=True)  # 班级外键

    __tablename__ = 'student'

    def __init__(self, name, age, sex, g_id):
        self.s_name = name
        self.s_age = age
        self.s_sex = sex
        self.grade = g_id

    def save(self):
        db.session.add(self)
        db.session.commit()


# 班级信息
class Grade(db.Model):
    g_id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 主键
    g_name = db.Column(db.String(20))  # 班级名称
    is_Delete = db.Column(db.Boolean, default=False)  # 逻辑删除
    student = db.relationship('Student', backref='stu', lazy=True)

    __tablename__ = 'grade'

    def __init__(self, name):
        self.g_name = name

    def save(self):
        db.session.add(self)
        db.session.commit()


# 权限角色中间表
sc = db.Table('sc',
              db.Column('j_id', db.Integer, db.ForeignKey('jurisdiction.j_id'), primary_key=True),
              db.Column('r_id', db.Integer, db.ForeignKey('roles.r_id'), primary_key=True)
              )


# 权限信息
class Jurisdiction(db.Model):
    j_id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 主键
    j_level = db.Column(db.String(16), unique=True)  # 权限级别
    roles = db.relationship('Roles', secondary=sc, backref='rs')  # 多对多关系字段

    __tablename__ = 'jurisdiction'


# 角色信息
class Roles(db.Model):
    r_id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 主键
    r_name = db.Column(db.String(16), unique=True)  # 角色名称
    user = db.relationship('User', backref='user', lazy=True)  # 关联用户表

    __tablename__ = 'roles'

    def __init__(self, name):
        self.r_name = name

    def save(self):
        db.session.add(self)
        db.session.commit()
