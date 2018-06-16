from flask import Blueprint, request, render_template, redirect, url_for, session
from AdminOs.models import db, User, Grade, Student, Jurisdiction, Roles
from utils.decorate import is_login

admin_blueprint = Blueprint('admin', __name__)


# 创建数据表
@admin_blueprint.route('/create_db/')
def create_db():
    db.create_all()

    return '创建成功'


# 用户注册
@admin_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        title = '注 册'
        path = 'register'
        return render_template('register.html', title=title, path=path)

    if request.method == 'POST':

        # 获取注册信息
        username = request.form.get('username')
        passwd1 = request.form.get('passwd1')
        passwd2 = request.form.get('passwd2')

        # 验证注册信息是否为空
        if not all([username, passwd1, passwd2]):
            msg = '请将注册信息填写完整'
            return render_template('register.html', msg=msg)

        # 验证两次输入密码是否一致
        if passwd1 != passwd2:
            msg = '两次输入密码不一致'
            return render_template('register.html', msg=msg)

        # 验证用户名长度
        if len(username) > 16:
            msg = '用户名长度超出合理范围'
            return render_template('register.html', msg=msg)

        # 创建并保存此用户
        user = User(username, passwd1)
        user.save()

        # 重定向到登录页面
        return redirect(url_for('admin.login'))


# 用户登录
@admin_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        title = '登 录'
        path = 'login'
        return render_template('login.html', title=title, path=path)

    if request.method == 'POST':
        uname = request.form.get('username')
        pwd = request.form.get('passwd1')

        if not all([uname, pwd]):
            msg = '请将登录信息填写完整'
            return render_template('login.html', msg=msg)

        user = User.query.filter_by(u_name=uname, u_pwd=pwd).first()
        if user:
            session['user_id'] = user.u_id
            return redirect(url_for('admin.index'))

        else:
            msg = '用户名或密码错误'
            return render_template('login.html', msg=msg)


# 班级列表

@admin_blueprint.route('/grade/', methods=['GET'])
@is_login
def grade():
    if request.method == 'GET':
        grade = Grade.query.all()
        flag = 1
        return render_template('grade.html', flag=flag, grade=grade)


# 添加班级

@admin_blueprint.route('/addgrade/', methods=['GET', 'POST'])
@is_login
def addgrade():
    if request.method == 'GET':
        return render_template('addgrade.html')

    if request.method == 'POST':
        grade_name = request.form.get('grade_name')
        grade = Grade(grade_name)
        grade.save()

        return redirect(url_for('admin.grade'))


# 学生列表

@admin_blueprint.route('/student/', methods=['GET'])
@is_login
def student():
    if request.method == 'GET':
        student = Student.query.all()
        flag = 1
        return render_template('student.html', flag=flag, student=student)


# 添加学生


@admin_blueprint.route('/addstu/', methods=['GET', 'POST'])
@is_login
def addstu():
    if request.method == 'GET':
        grades = Grade.query.all()
        return render_template('addstu.html', grades=grades)

    if request.method == 'POST':
        name = request.form.get('addstu_name')
        age = request.form.get('addstu_age')
        sex = True if request.form.get('addstu_sex') else False
        g_id = request.form.get('addstu_grade')

        stu = Student(name=name, age=age, sex=sex, g_id=g_id)
        stu.save()

        return redirect(url_for('admin.student'))


# 权限列表

@admin_blueprint.route('/permissions/', methods=['GET'])
@is_login
def roles():
    if request.method == 'GET':
        flag = 1
        jurisdiction = Jurisdiction.query.all()
        return render_template('permissions.html', jurisdiction=jurisdiction, flag=flag)


# 添加权限
@admin_blueprint.route('/addpermission/', methods=['POST', 'GET'])
def addpermission():
    if request.method == 'GET':
        jurisdiction = Jurisdiction.query.all()
        user = User.query.all()
        return render_template('addpermission.html', jurisdiction=jurisdiction, user=user)


# 角色列表
@admin_blueprint.route('/roles/', methods=['GET'])
@is_login
def permissions():
    if request.method == 'GET':
        roles = Roles.query.all()
        return render_template('roles.html', roles=roles)


# 添加角色
@admin_blueprint.route('/addroles/', methods=['GET', 'POST'])
@is_login
def addroles():
    if request.method == 'GET':
        return render_template('addroles.html')

    if request.method == 'POST':
        roles_name = request.form.get('roles_name')
        rolesThis = Roles(roles_name)
        rolesThis.save()


# 用户列表
@admin_blueprint.route('/users/', methods=['GET'])
@is_login
def users():
    if request.method == 'GET':
        user = User.query.all()
        flag = 1
        return render_template('users.html', flag=flag, user=user)


# 权限管理


@admin_blueprint.route('/left/', methods=['GET'])
@is_login
def left():
    if request.method == 'GET':
        user_id = session.get('user_id')
        longpermission = len(User.query.filter_by(u_id=user_id).first().user.rs)
        level = 0
        if longpermission == 2:
            level = 1
        elif longpermission == 4:
            level = 2
        elif longpermission == 5:
            level = 3
        return render_template('left.html', level=level)


# 退出
@admin_blueprint.route('/logout/', methods=['GET'])
def logout():
    session.pop('user_id')
    return render_template('login.html')


# 添加用户
@admin_blueprint.route('/add_edit/', methods=['GET', 'POST'])
@is_login
def add_edit():
    if request.method == 'GET':
        roles = Roles.query.all()
        return render_template('add_edit.html', roles=roles)

    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        r_id = int(request.form.get('r_id'))

        # 验证添加信息是否完整
        if not all([username, password1, password2]):
            msg = '请提交完整信息'
            return render_template('add_edit.html', msg=msg)

        # 验证两次输入密码是否一致
        if password2 != password1:
            msg = '两次输入密码不一致'
            return render_template('add_edit.html', msg=msg)

        # 验证ID正确性
        if not 1 <= r_id <= 3:
            msg = '权限ID不在合理范围内'
            return render_template('add_edit.html', msg=msg)

        user_now = User(name=username, pwd=password1, r_id=r_id)
        user_now.save()
        
        return redirect(url_for('admin.users'))


# 管理系统首页

@admin_blueprint.route('/index/', methods=['GET'])
@is_login
def index():
    if request.method == 'GET':
        return render_template('index.html')


@admin_blueprint.route('/head/', methods=['GET'])
@is_login
def head():
    if request.method == 'GET':
        user_name = User.query.filter_by(u_id=session.get('user_id')).first().u_name
        return render_template('head.html', user_name=user_name)


@admin_blueprint.route('/main/', methods=['GET'])
@is_login
def main():
    if request.method == 'GET':
        flag = 2
        return render_template('main.html', flag=flag)
