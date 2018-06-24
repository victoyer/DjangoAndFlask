from flask import Blueprint, request, render_template, jsonify, session, url_for, redirect
from aj_user.models import User
import re
import os
from utils import status_code
from utils.ModFilter import is_login
from utils.setting import UPLOAD_DIR
from aj_user.models import db

# 创建蓝图
aj_user = Blueprint('user', __name__)


@aj_user.route('/create_db/')
def create_db():
    db.create_all()
    return '创建成功'


# 用户注册
@aj_user.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@aj_user.route('/register/', methods=['POST'])
def user_register():
    # 获取用户注册信息
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    # 验证用户注册信息是否为空
    if not all([mobile, password, password2]):
        return jsonify(status_code.USER_REGISTER_DATA_NOT_NULL)

    # 验证手机号
    if not re.match(r'^1[34578]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)

    # 验证两次输入密码是否一致
    if password != password2:
        return jsonify(status_code.USER_REGISTER_PASSWORD_IS_NOT_VALID)

    # 保存用户数据
    user = User.query.filter_by(phone=mobile).first()
    if user:
        return jsonify(status_code.USER_REGISTER_MOBILE_EXISTS)

    else:
        user = User()
        user.phone = mobile
        user.password = password
        user.name = mobile
        user.add_update()

        return jsonify(status_code.SUCCESS)


# 用户登录
@aj_user.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@aj_user.route('/login/', methods=['POST'])
def user_login():
    mobile = request.form.get('mobile')
    password = request.form.get('password')

    # 验证登录信息是否为空
    if not all([mobile, password]):
        return jsonify(status_code.USER_LOGIN_DATA_NOT_NULL)

    # 验证用户名
    user = User.query.filter_by(phone=mobile).first()
    if user:
        # 验证密码
        if not user.check_pwd(password):
            return jsonify(status_code.USER_LOGIN_PASSWORD_IS_NOT_VALID)

        # 验证用户成功
        session['user_id'] = user.id
        return jsonify(status_code.SUCCESS)

    else:
        return jsonify(status_code.USER_LOGIN_USER_NOT_EXISTS)


# 退出登录
@aj_user.route('/logout/', methods=['GET'])
@is_login
def logout():
    session.clear()
    # return redirect(url_for('user.login'))
    return jsonify(status_code.SUCCESS)


# 个人中心
@aj_user.route('/my/', methods=['GET'])
@is_login
def my():
    return render_template('my.html')


# 修改个人信息
@aj_user.route('/profile/', methods=['GET'])
@is_login
def profile():
    return render_template('profile.html')


@aj_user.route('/profile_info/', methods=['GET'])
def user_info():
    # 获取当前用户对象
    user = User.query.filter_by(id=session.get('user_id')).first()

    # 返回用户名和头像
    return jsonify({'data': user.to_basic_dict()})


@aj_user.route('/profile_img/', methods=['POST'])
@is_login
def user_profile():
    file = request.files.get('avatar')
    if not re.match(r'image/.*', file.mimetype):
        return jsonify(status_code.USER_CHANGE_PROFILE_IMAGE)

    # 保存图片到项目img目录

    file.save(os.path.join(UPLOAD_DIR, file.filename))

    # 保存图片相对路径到数据库

    # 获取图片相对路径
    img_path = os.path.join('img', file.filename)
    # 获取当前登录用户对象
    user = User.query.filter_by(id=session.get('user_id')).first()

    # 保存此路径到数据库
    user.avatar = img_path

    # 捕获保存用户更改头像的异常
    try:
        user.add_update()

    except Exception as e:
        db.session.rollback()
        return jsonify(status_code.USER_UPDATE_MYSQL_NO)

    return jsonify({'code': '200', 'msg': img_path})


@aj_user.route('/profile_name/', methods=['POST'])
@is_login
def user_name():
    # 获取提交用户名
    uname = request.form.get('name')

    # 获取当前用户对象
    user = User.query.filter_by(id=session.get('user_id')).first()

    # 判断要更新的用户名是否存在
    if User.query.filter_by(name=uname).first():
        return jsonify(status_code.USER_UPDATE_NAME_EXISTENCE)

    # 更改用户名
    user.name = uname

    # 捕获保存用户更改用户名的异常
    try:
        user.add_update()

    except Exception as e:
        db.session.rollback()
        return jsonify(status_code.USER_UPDATE_MYSQL_NO)

    return jsonify({'code': '200', 'msg': uname})

    # return redirect(url_for('user.my'))


# 实名认证
@aj_user.route('/auth/', methods=['GET'])
@is_login
def auth():
    return render_template('auth.html')


# 创建实名认证信息
@aj_user.route('/auth/', methods=['POST'])
@is_login
def auth_info():
    # 获取提交的实名认证信息
    really_name = request.form.get('iname')
    really_card = request.form.get('icard')

    # 验证信息是否完整
    if not all([really_card, really_name]):
        return jsonify(status_code.USER_AUTH_IS_NOT_NULL)

    # 验证身份证
    if not re.match(r'^[1-9]\d{17}$', really_card):
        return jsonify(status_code.USER_AUTH_ID_CARD_IS_NOT_VALID)

    # 获取当前用户对象
    user = User.query.filter_by(id=session.get('user_id')).first()
    # 保存认证信息
    user.id_name = really_name
    user.id_card = really_card

    # 保存用户认证信息到数据库
    try:
        user.add_update()
    except Exception as e:
        # 出现异常回滚事务
        db.session.rollback()
        return jsonify(status_code.USER_UPDATE_MYSQL_NO)

    return jsonify(status_code.SUCCESS)


# 获取实名认证信息
@aj_user.route('/auth_info/', methods=['GET'])
@is_login
def auths():
    user = User.query.filter_by(id=session.get('user_id')).first()
    return jsonify({'code': '200', 'msg': user.to_auth_dict()})



