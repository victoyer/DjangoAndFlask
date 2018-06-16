from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from app.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, OrderModel, OrderGoodsModel
from django.core.urlresolvers import reverse
from app.models import FoodType, Goods, CartModel
from user.models import UserTicketModel
from utils.function import get_order_random_id


def home(request):
    # 首页视图函数
    if request.method == 'GET':
        # 从Mysql获取数据
        mainwheel = MainWheel.objects.all()
        mainnav = MainNav.objects.all()
        mainmustbuy = MainMustBuy.objects.all()
        mainshop = MainShop.objects.all()
        mainshow = MainShow.objects.all()

        # 切片
        # mainshop1 = mainshop[:1]
        # mainshop2_4 = mainshop[1:3]
        # mainshop5_8 = mainshop[3:7]
        # mainshop9_11 = mainshop[7:]

        data = {
            'title': '首页',
            'mainwheel': mainwheel,
            'mainnav': mainnav,
            'mainmustbuy': mainmustbuy,
            'mainshop': mainshop,
            'mainshow': mainshow

        }
        return render(request, 'home/home.html', data)


def mine(request):
    # 个人中心
    if request.method == 'GET':

        user = request.user
        orders = OrderModel.objects.filter(user=user)
        payed, wait_pay = 0, 0
        for order in orders:
            if order.o_status == 0:
                wait_pay += 1

            if order.o_status == 1:
                payed += 1

        data = {
            'payed': payed,
            'wait_pay': wait_pay
        }

        return render(request, 'mine/mine.html', data)


def market(request):
    # 闪购列表页
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('axf:market_params', args=('104749', '0', '0')))


def user_market(request, typeid, cid, sid):
    """
    :param typeid: 分类ID
    :param cid: 子分类ID
    :param sid: 排序ID
    """
    if request.method == 'GET':
        # 获取分类名称全部信息
        foodtypes = FoodType.objects.all()

        # 判断传入的子类ID查询数据，0查询全部数据
        if cid == '0':

            goods = Goods.objects.filter(categoryid=typeid)

        else:
            goods = Goods.objects.filter(categoryid=typeid, childcid=cid)

        # 查找当前选择的分类的所有字段
        foodstype_current = foodtypes.filter(typeid=typeid).first()

        # 获取当前分类的子分类数据并且按照 # 号分割
        foodschildcidname = foodstype_current.childtypenames.split('#')

        # 定义一个储存分割结果的列表
        chlid_list = []

        for chlidtypename in foodschildcidname:
            # 把按照 # 号分割的数据再用 : 号分割
            chlid_type_info = chlidtypename.split(':')

            # 把结果添加到已定义列表
            chlid_list.append(chlid_type_info)

        # 排序
        if sid == '0':
            # 综合排序
            pass
        if sid == '1':
            # 销量排序
            goods = goods.order_by('productnum')

        if sid == '2':
            # 价格升序
            goods = goods.order_by('-price')

        if sid == '3':
            # 价格降序
            goods = goods.order_by('price')

        data = {
            'foodtypes': foodtypes,
            'goods': goods,
            'typeid': typeid,
            'chlid_list': chlid_list,
            'cid': cid
        }
        return render(request, 'market/market.html', data)


# 添加商品
def add_cart(request):
    if request.method == 'POST':

        # 获取当前用户
        user = request.user

        # 获取前端POST的当前商品ID
        goods_id = request.POST.get('goods_id')

        # 定义返回Json格式
        data = {
            'code': 200,
            'msg': '请求成功'
        }

        # 判断用户是系统自带的还是登录用户
        if user.id:

            # 是登录用户就根据商品ID和用户获取一个购物车对象
            user_cart = CartModel.objects.filter(user=user, goods_id=goods_id).first()

            # 判断是否有购物车对象
            if user_cart:

                # 有的话商品数量加一
                user_cart.c_num += 1

                # 保存进数据库
                user_cart.save()

                # 插入返回json数据
                data['c_num'] = user_cart.c_num

            else:
                # 没有购物车对象，进行创建
                CartModel.objects.create(user=user, goods_id=goods_id)

                data['c_num'] = 1

            return JsonResponse(data)
        data['code'] = 403
        data['msg'] = '当前用户未登录'
        return JsonResponse(data)


# 减少购物车用户下单商品的数量
def sub_cart(request):
    data = {
        'code': 200,
        'msg': '请求成功'
    }

    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        user = request.user

        if user.id:

            # 获取用户下单对应的信息
            user_cart = CartModel.objects.filter(user=user, goods_id=goods_id).first()

            # 判断购物车有无此商品数据
            if user_cart:

                # 购物车已存在商品信息
                if user_cart:
                    # 如果购物车商品只剩下最后一个
                    if user_cart.c_num == 1:
                        # 删除当前商品所有信息
                        user_cart.delete()
                        # 商品数量重置为0
                        data['c_num'] = 0

                    else:
                        # 商品数量大于一个就减一
                        user_cart.c_num -= 1
                        # 保存数据到数据库
                        user_cart.save()
                        # 把减少后的商品数量添加到返回数据
                        data['c_num'] = user_cart.c_num

                    # 返回数据
                    return JsonResponse(data)

            else:
                # 购物车中无此商品信息
                data['msg'] = '购物车中无此商品信息'
                data['code'] = 403
                return JsonResponse(data)

        # 未登录
        else:
            data['msg'] = '请先登录'
            data['code'] = 403

        return JsonResponse(data)


# 查询购物车信息
def infoCart(request):
    user_cookie = UserTicketModel.objects.filter(ticket=request.COOKIES.get('ticket')).first().user
    user_cart = CartModel.objects.filter(user=user_cookie)
    info = []
    for data in user_cart:
        info.append([data.goods_id, data.c_num])
        # goods_id.append(data.goods_id)
        # c_num.append(data.c_num)

    if user_cookie:
        data = {
            'code': 200,
            'msg': '请求成功',
            'info': info
            # 'goods_id': goods_id,
            # 'c_num': c_num

        }

    else:
        data = {
            'code': 403,
            'msg': '请先登录'
        }

    return JsonResponse(data)


def cart(request):
    if request.method == 'GET':
        # 获取用户信息
        user = request.user

        # 获取当前用户的购物车
        user_cart = CartModel.objects.filter(user=user)

        data = {
            'user_cart': user_cart,
        }

        return render(request, 'cart/cart.html', data)


def change_select_status(request):
    """
    选择商品状态
    """
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        cart = CartModel.objects.filter(id=cart_id).first()
        if cart.is_selcet:
            cart.is_selcet = False
        else:
            cart.is_selcet = True
        cart.save()
        data = {
            'code': 200,
            'msg': '请求成功',
            'is_select': cart.is_selcet
        }
        return JsonResponse(data)


# 全选或全不选商品
# def totalchoice(request):
#     if request.method == 'POST':
#         # 获取request中POST传入的ID，根据此ID查找对应的CartModel对象
#         id = request.POST.get('id')
#         cart_list = CartModel.objects.filter(user=request.user)
#         if id == '1':
#             for cart in cart_list:
#                 cart.is_selcet = False
#                 cart.save()
#         else:
#             for cart in cart_list:
#                 cart.is_selcet = True
#
#         return JsonResponse({'code': 200, 'cart_is_selcet': cart_list.first().is_selcet})

        # for cart in cart_list:
        #     if cart.is_selcet:
        #         pass
        #
        # # 判断此对象是否选中
        # if cart.is_selcet:
        #     # 选中被点击改为不选中
        #     cart.is_selcet = False
        # else:
        #     # 不选中点击改为选中
        #     cart.is_selcet = True
        #
        # cart.save()
        # data = {
        #     'code': 200,
        #     'msg': '请求成功',
        #     'is_selcet': cart.is_selcet
        # }
        # return JsonResponse(data)


def generate_order(request):
    """
       下单操作
       """
    if request.method == 'GET':
        user = request.user
        # 创建订单
        o_num = get_order_random_id()
        order = OrderModel.objects.create(user=user, o_num=o_num)
        # 选择勾选的商品进行下单
        user_carts = CartModel.objects.filter(user=user, is_selcet=True)

        for carts in user_carts:
            #  创建商品和订单之间的关系
            OrderGoodsModel.objects.create(goods=carts.goods,
                                           orders=order,
                                           goods_num=carts.c_num)

        # 下单成功要删除购物车的数据
        user_carts.delete()

        return render(request, 'order/order_info.html', {'order': order})


def changeOrder(request):
    # 修改订单状态
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        OrderModel.objects.filter(id=order_id).update(o_status=1)
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def order_wait_pay(request):
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user=user, o_status=0)
        return render(request, 'order/order_list_wait_pay.html', orders)
