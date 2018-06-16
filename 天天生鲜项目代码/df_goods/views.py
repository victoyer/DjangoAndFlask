from django.core.paginator import Paginator
from django.shortcuts import render
from df_goods.models import GoodsType, Goods


def cart(request):
    if request.method == 'GET':
        data = {
            'flag': 2,
            'subtitle': '购物车',
            'title': '购物车'
        }
        return render(request, 'df_goods/cart.html', data)


def detail(request, id):
    if request.method == 'GET':
        goods_detail = Goods.objects.filter(pk=id).first()

        # 商品点击数加一
        goods_detail.gclick = goods_detail.gclick + 1
        goods_detail.save()

        # 最新两个商品
        news = goods_detail.gtype.goods_set.order_by('-id')[0:2]

        data = {
            'flag': 1,
            'title': '商品详情',
            'news': news,
            'goods_detail': goods_detail,
            'id': id
        }
        response = render(request, 'df_goods/detail.html', data)

        # 最近浏览商品(五个)
        goods_ids = request.COOKIES.get('goods_ids', '')

        # 判断是否有浏览记录
        if goods_ids:
            # 有浏览记录按，分割
            goods_list = goods_ids.split(',')

            # 判断当前商品是否已被记录
            if goods_list.count(str(id)) >= 1:
                goods_list.remove(id)

            # 添加当前被点击商品ID到列表最前
            goods_list.insert(0, id)

            # 显示最近浏览的列表的数量为五

            if len(goods_list) >= 6:
                del goods_list[5]

            # 拼接回goods_ids
            goods_ids = ','.join(goods_list)

        # 没有浏览记录添加当前商品ID进入列表
        else:
            goods_ids = id

        # 写入cookie
        response.set_cookie('goods_ids', goods_ids)

        # 返回结果
        return response


def list(request, tid, pindex, sort):
    # /xx/tid/poindex/sort/
    if request.method == 'GET':
        # 获取最新的两条数据
        typeinfo = GoodsType.objects.filter(id=tid).first()
        news = typeinfo.goods_set.order_by('-id')[0:2]

        # 排序
        if sort == '1':  # 默认 - 最新
            goods_list = Goods.objects.filter(gtype_id=int(tid)).order_by('-id')

        elif sort == '2':  # 价格
            goods_list = Goods.objects.filter(gtype_id=int(tid)).order_by('-gprice')

        elif sort == '3':  # 销量
            goods_list = Goods.objects.filter(gtype_id=int(tid)).order_by('-gclick')

        # 分页
        paginator = Paginator(goods_list, 10)
        page = paginator.page(int(pindex))

        data = {
            'flag': 1,
            'title': typeinfo.typename,
            # 'goods_list': goods_list,
            'paginator': paginator,
            'page': page,
            'sort': sort,
            'news': news,
            'typeinfo': typeinfo,

        }
        return render(request, 'df_goods/list.html', data)


def placeOrder(request):
    if request.method == 'GET':
        data = {
            'flag': 2,
            'subtitle': '提交订单',
            'title': '提交订单'
        }
        return render(request, 'df_goods/place_order.html', data)


def index(request):
    if request.method == 'GET':
        # 查询所有商品类型
        typeall = GoodsType.objects.all()
        # 查询每一类商品最新的四条数据
        type_now0 = typeall[0].goods_set.order_by('-id')[0:4]
        type_heat0 = typeall[0].goods_set.order_by('-gclick')[0:4]

        type_now1 = typeall[1].goods_set.order_by('-id')[0:4]
        type_heat1 = typeall[1].goods_set.order_by('-gclick')[0:4]

        type_now2 = typeall[2].goods_set.order_by('-id')[0:4]
        type_heat2 = typeall[2].goods_set.order_by('-gclick')[0:4]

        type_now3 = typeall[3].goods_set.order_by('-id')[0:4]
        type_heat3 = typeall[3].goods_set.order_by('-gclick')[0:4]

        type_now4 = typeall[4].goods_set.order_by('-id')[0:4]
        type_heat4 = typeall[4].goods_set.order_by('-gclick')[0:4]

        type_now5 = typeall[5].goods_set.order_by('-id')[0:4]
        type_heat5 = typeall[5].goods_set.order_by('-gclick')[0:4]

        data = {
            'flag': 1,
            'title': '首页',
            'type_now0': type_now0,
            'type_heat0': type_heat0,
            'type_now1': type_now1,
            'type_heat1': type_heat1,
            'type_now2': type_now2,
            'type_heat2': type_heat2,
            'type_now3': type_now3,
            'type_heat3': type_heat3,
            'type_now4': type_now4,
            'type_heat4': type_heat4,
            'type_now5': type_now5,
            'type_heat5': type_heat5,
        }
        return render(request, 'df_goods/index.html', data)


# 商品信息获取路径
def info(request):
    if request.method == 'POST':
        pass
