from django.shortcuts import render
from df_cart.models import CartInfo
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse


def cart(request):
    if request.method == 'GET':
        data = {
            'flag': 2,
            'subtitle': '购物车',
            'title': '购物车'
        }
        return render(request, 'df_goods/cart.html', data)


def addcart(request, gid, count):
    if request.method == 'GET':

        # 获取当前登录的用户ID
        uid = request.user.id
        # 获取当前选择的商品ID
        gid = int(gid)

        # 用商品ID和用户ID查找购物车
        carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)

        if len(carts) >= 1:

            # 购物车有此商品数量加
            cart = carts[0]
            cart.count = cart.count + int(count)

        else:
            # 购物车无此商品就创建此商品
            CartInfo.objects.create_cart(uid=uid, gid=gid, count=count)

    # 如果请求是ajax来的
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.user.id).count()
        return JsonResponse({'count': count})

    # return HttpResponseRedirect('')
