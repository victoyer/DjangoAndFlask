from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.deprecation import MiddlewareMixin
from datetime import datetime
from df_user.models import UserTicket, UserInfo


# 定义一个中间件类去验证是否登录以及登录用户的ticket是否过期，再把此用户对象赋值到request
class UserAuthMiddle(MiddlewareMixin):

    # 每个请求都会通过process_request函数
    def process_request(self, request):
        # 需要验证登录ticket的路径
        VerificationPath = ['/user/register/', '/user/login/', '/user/logout/']

        if not request.path in VerificationPath:

            # 先获取request中COOKIES的ticket
            ticket = request.COOKIES.get('ticket')

            # 再通过获取ticket获取对应的用户
            user_ticket = UserTicket.objects.filter(ticket=ticket).first()

            # 判断是否获取到ticket对应的用户
            if user_ticket:

                # 如果用户登录的ticket已经过期
                if datetime.now() > user_ticket.out_time.replace(tzinfo=None):
                    # 删除掉这个ticket记录
                    UserTicket.objects.filter(user=user_ticket.user).delete()

                    # 重定向到用户登录界面

                    return HttpResponseRedirect(reverse('user:login'))

                # 如果用户登录的ticket没有过期
                else:
                    # 把user对象赋值给request
                    request.user = user_ticket.user

                    # 删除多余的ticket登录信息
                    UserTicket.objects.filter(Q(user=user_ticket.user) & ~Q(ticket=ticket)).delete()

                    return None

            # 没有获取到ticket对应用户
            else:
                return HttpResponseRedirect(reverse('user:login'))


        # 不需要验证ticket的路径
        else:
            return None
