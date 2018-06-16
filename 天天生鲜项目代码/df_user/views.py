from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from df_user.models import UserInfo, UserTicket
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from utils.functions import randomCode
from datetime import datetime, timedelta
from df_goods.models import Goods


# 用户注册


def register(request):
    if request.method == 'GET':
        return render(request, 'df_user/register.html')

    if request.method == 'POST':

        # 获取用户注册信息
        uname = request.POST.get('user_name')
        upwd = request.POST.get('pwd')
        cupwd = request.POST.get('cpwd')
        uemail = request.POST.get('email')

        # 验证所有参数是否为空
        if not all([uname, upwd, cupwd, uemail]):
            data = {'msg': '请将注册信息填写完整', 'title': '用户注册'}
            return render(request, 'df_user/register.html', data)

        # 验证密码是否一致
        if upwd != cupwd:
            # 密码不一致返货注册页面
            return HttpResponseRedirect(reverse('user:register'))

        # 密码一致加密密码
        passwd = make_password(upwd)

        # 创建用户信息
        UserInfo.objects.create(uname=uname, upwd=passwd, uemail=uemail)

        # 重定向去登录页面
        return HttpResponseRedirect(reverse('user:login'))


# 用户登录
def login(request):
    if request.method == 'GET':
        return render(request, 'df_user/login.html')

    if request.method == 'POST':
        uname = request.POST.get('username')  # 登录用户名
        upwd = request.POST.get('pwd')  # 登录密码

        # 判定数据是否为空
        if not all([uname, upwd]):
            data = {'msg': '请将登录信息填写完整', 'title': '用户登录'}
            return render(request, 'df_user/login.html', data)

        # 查找数据库确认是否存在此用户
        user = UserInfo.objects.filter(uname=uname).first()

        # 存在此用户确认密码是否正确
        if user:
            if check_password(upwd, user.upwd):
                # 用户名正确保存ticket到浏览器ticket
                ticket = randomCode()
                # 1. 获取返回的response
                response = HttpResponseRedirect(reverse('goods:index'))

                # 2.获取系统时间并使用timedelta函数加一天时间为ticket过期时间
                out_time = datetime.now() + timedelta(days=1)

                # 3.保存ticket到浏览器
                response.set_cookie('ticket', ticket, expires=out_time)

                # 4.保存ticket到数据库
                UserTicket.objects.create(user=user, ticket=ticket, out_time=out_time)

                # 返回response对象
                return response

        return render(request, 'df_user/login.html', {'msg': '用户名或密码错误', 'title': '用户登录'})


# 验证用户名
def VerUserName(request):
    if request.method == 'POST':
        user_name = request.POST.get('uname')
        count = UserInfo.objects.filter(uname=user_name).count()
        data = {'count': count}
        return JsonResponse(data)


# 用户退出
def logout(request):
    if request.method == 'GET':
        request.COOKIES.clear()
        return HttpResponseRedirect(reverse('user:login'))


#
# # 首页
# def index(request):
#     if request.method == 'GET':
#         return render(request, 'index/index.html')
#     return HttpResponseRedirect('')


# 用户个人信息
def UserCenterInfo(request):
    if request.method == 'GET':
        # 最近浏览信息
        # 商品ID
        goods_ids = request.COOKIES.get('goods_ids', '').split(',')

        # 商品实例对象
        goods_list = Goods.objects.filter(id__in=goods_ids)

        data = {'flag': 1,
                'title': '个人中心',
                'goods_list': goods_list
                }
        return render(request, 'df_user/user_center_info.html', data)


# 用户订单信息
def UserCenterOrder(request):
    if request.method == 'GET':
        data = {'flag': 1,
                'title': '订单信息'

                }
        return render(request, 'df_user/user_center_order.html', data)


# 用户收货地址信息
def UserCeenterSite(request):
    if request.method == 'GET':
        data = {'flag': 1,
                'title': '收货地址'
                }
        return render(request, 'df_user/user_center_site.html', data)
