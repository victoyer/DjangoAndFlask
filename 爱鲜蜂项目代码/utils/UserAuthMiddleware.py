from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.core.urlresolvers import reverse
from user.models import UserTicketModel, UserModel
from datetime import datetime


# 定义一个中间件类继承MiddlewareMixin
class UserAuthMiddle(MiddlewareMixin):

    def process_request(self, request):

        # 拿到request中的path路径

        # 需要登录验证的路径
        no_login = ['/axf/mine/', '/axf/addCart/', '/axf/subCart/', '/axf/cart/', '/axf/totalchoice/',
                    '/axf/generateOrder/', '/axf/order_wait_pay/']

        # 判断路径是否验证ticket

        if request.path in no_login:

            # 从request.cookie中获取ticket
            ticket = request.COOKIES.get('ticket')

            # 没有ticket返回登录页面
            if not ticket:
                return HttpResponseRedirect(reverse('user:login'))

            # request有ticket去验证数据库的ticket
            user_ticket = UserTicketModel.objects.filter(ticket=ticket).first()

            # 判断数据库中是否有这个ticket
            # 没有返回登录页面
            if not user_ticket:
                return HttpResponseRedirect(reverse('user:login'))

            else:
                # 判断当前ticker的时间有没有过期
                if datetime.now() < user_ticket.out_time.replace(tzinfo=None):
                    # 在ticket表通过外键找到当前登录user,把当前登录user多余的ticket找出来删掉
                    UserTicketModel.objects.filter(Q(user=user_ticket.user) & ~Q(ticket=ticket)).delete()

                else:
                    # 过期-在ticket表通过外键找到当前登录user删除，返回登录界面
                    UserTicketModel.objects.filter(user=user_ticket.user).delete()
                    return HttpResponseRedirect(reverse('user:login'))

            # 把ticket绑定到全局相应request
            request.user = user_ticket.user

        else:
            return None
