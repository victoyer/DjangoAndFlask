from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from user.models import UserModel, UserTicketModel
from utils.function import get_ticket


def register(request):
    # 用户注册
    if request.method == 'GET':
        return render(request, 'user/user_register.html')

    if request.method == 'POST':
        username = request.POST.get('username')  # 用户名
        email = request.POST.get('email')  # 用户邮箱
        password = request.POST.get('password')  # 用户密码
        icon = request.FILES.get('icon')  # 用户头像

        # all()验证参数都不为空
        if not all([username, email, password, icon]):
            # 验证不通过, 提示参数不能为空，向页面返回错误信息
            msg = '请将注册信息填写完整'
            # 返回注册页面
            return render(request, 'user/user_register.html', {'msg': msg})

        # 加密password
        password = make_password(password)

        # 所有参数都有创建用户
        UserModel.objects.create(username=username,
                                 password=password,
                                 email=email,
                                 icon=icon
                                 )
        # 返回登录页面
        return redirect('user:login')


def login(request):
    # 用户登录
    if request.method == 'GET':
        # get请求返回页面
        return render(request, 'user/user_login.html')

    if request.method == 'POST':

        # post请求获取用户名和密码
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 对数据库查询此用户对象实例
        user = UserModel.objects.filter(username=username).first()

        # 查询实例存在
        if user:
            # 验证密码正确
            if check_password(password, user.password):

                # 1、保存ticket在客户端
                # 自定义ticket模块生成ticket并获取
                ticket = get_ticket()

                # 保存返回的HttpResponse对象
                response = HttpResponseRedirect(reverse('axf:mine'))

                # 定义过期时间
                out_time = datetime.now() + timedelta(days=1)

                # 设置返回HpptRespouse对象的cookie
                response.set_cookie('ticket', ticket, expires=out_time)

                # 2、保存到ticket服务端的user_ticket表中
                UserTicketModel.objects.create(user=user,
                                               out_time=out_time,
                                               ticket=ticket)

                # 返回HttpResponse对象
                return response

            else:
                msg = '用户名或密码错误'
                return render(request, 'user/user_login.html', {'msg': msg})

        else:
            msg = '用户名或密码错误'
            return render(request, 'user/user_login.html', {'msg': msg})


def logout(request):
    # 用户登出，删除当前登录的用户的cookie中ticket的信息
    if request.method == 'GET':
        # 获取Http返回的request
        response = HttpResponseRedirect(reverse('user:login'))
        # 删除返回request的ticket
        response.delete_cookie('ticket')
        # 返回request
        return response
