from flask import Blueprint, session, render_template, request, url_for, jsonify
from datetime import datetime
from aj_user.models import House, Order, db, User, Area
from utils import status_code
from utils.ModFilter import is_login

# 注册蓝图
aj_order = Blueprint('order', __name__)


@aj_order.route('/suborder/', methods=['POST'])
@is_login
def suborder():
    # 获取提交信息
    beginDate = request.form.get('beginData')
    endDate = request.form.get('endData')
    house_id = request.form.get('house_id')

    # 验证数据不能为空
    if not all([beginDate, endDate, house_id]):
        return jsonify(status_code.ORDER_DATA_IS_NOT_NULL)

    # 住房起始时间不能大于结束时间
    if beginDate > endDate:
        return jsonify(status_code.ORDER_DATA_DATETIME_ERROR)

    # 住房日期转换格式
    beginDate = datetime.strptime(beginDate, '%Y-%m-%d')
    endDate = datetime.strptime(endDate, '%Y-%m-%d')

    # 获取当前房源的对象
    house = House.query.get(house_id)

    # 创建订单对象并保存
    order = Order()
    order.user_id = session.get('user_id')
    order.house_id = house_id
    order.begin_date = beginDate
    order.end_date = endDate
    order.days = int((endDate - beginDate).days) + 1
    order.house_price = house.price
    order.amount = order.days * order.house_price
    order.add_update()

    return jsonify(status_code.SUCCESS)


# 访问我的订单
@aj_order.route('/orders/', methods=['GET'])
@is_login
def orders():
    return render_template('orders.html')


# 返回当前用户的订单数据
@aj_order.route('/ordersinfo/', methods=['GET'])
@is_login
def ordersinfo():
    # 查询当前用户的订单数据
    myOrders = Order.query.filter_by(user_id=session.get('user_id')).all()

    # 序列化查询出的所有订单数据
    myOrders_list = [order.to_dict() for order in myOrders]

    return jsonify({'code': '200', 'msg': myOrders_list})


# 访问客户订单
@aj_order.route('/lorders/', methods=['GET'])
@is_login
def lorders():
    return render_template('lorders.html')


# 返回客户订单数据
@aj_order.route('/lordersinfo/', methods=['GET'])
@is_login
def lordersinfo():
    # # 查询当前用户的所有房源客户订单信息
    # for lorders in House.query.filter_by(user_id=session.get('user_id')):
    #     lorders_list = [lorder.to_dict for lorder in lorders.orders]
    #
    # # 返回所有查询出的数据
    # return jsonify({'code': '200', 'msg': lorders_list})

    # 查询当前用户的所有房源信息
    houses = House.query.filter_by(user_id=session.get('user_id'))

    # 获取所有房源ID
    house_ids = [house.id for house in houses]

    # 根据房源ID去查询订单信息,按订单ID降序排列
    orders = Order.query.filter(Order.house_id.in_(house_ids)).order_by(Order.id.desc())

    # 将查询出的房源信息序列化
    order_infos = [order.to_dict() for order in orders]

    # 返回查询结果
    return jsonify({'code': '200', 'msg': order_infos})


# 订单状态修改
@aj_order.route('/accept_order/', methods=['PATCH'])
@is_login
def accept_order():
    # 获取前端传入的值
    status = request.form.get('status')
    order_id = request.form.get('order_id')

    # 获取订单对象改变订单状态
    order = Order.query.get(order_id)
    order.status = status

    # 如果是拒单
    if status == 'REJECTED':
        order.comment = request.form.get('comment')

    try:
        # 保存修改
        order.add_update()

    except:
        # 执行操作失败进行回滚,并返回数据库错误状态码
        db.session.rollback()
        return jsonify(status_code.DATABASEERROR)
    # 返回状态码
    return jsonify(status_code.SUCCESS)


# 首页
@aj_order.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


# 首页返回信息
@aj_order.route('/hindex/', methods=['GET'])
def hindex():
    # 判断用户已登录就返回用户名
    username = ''
    if 'user_id' in session:
        username = User.query.get(session.get('user_id')).name

    # 获取房源信息,最多五条
    houses_info = House.query.order_by(House.id.desc()).all()[:5]

    # 序列化房源信息
    houses = [house.to_full_dict() for house in houses_info]

    # 获取城区信息返回json
    area_list_infos = [area.to_dict() for area in Area.query.all()]
    # area_list_infos = [area.to_dict() for area in area_list]

    # 返回获取到的信息
    return jsonify({'code': '200', 'username': username, 'area_list_infos': area_list_infos, 'houses': houses})


# 搜索
@aj_order.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')


@aj_order.route('/house_search/', methods=['GET'])
def house_search():
    # 获取get请求传递的所有参数
    search_info = request.args

    # 获取需要的参数
    aid = search_info.get('aid')  # 区域ID
    sd = search_info.get('sd')  # 开始时间
    ed = search_info.get('ed')  # 结束时间

    # 根据区域ID查询房源信息,不包括自己的房源
    houses = House.query.filter(House.area_id == aid)

    # 过滤到房东信息
    if "user_id" in session:
        houses = houses.filter(House.user_id != session['user_id'])

    # 根据房源ID查询订单信息, 已有订单不包括
    order1 = Order.query.filter(sd >= Order.begin_date, ed <= Order.begin_date).all()
    order2 = Order.query.filter(sd <= Order.begin_date, ed >= Order.end_date).all()
    order3 = Order.query.filter(sd <= Order.begin_date, ed >= Order.end_date).all()
    order4 = Order.query.filter(sd <= Order.begin_date, ed <= Order.end_date).all()

    # 去重
    order_info_list = [order_id.house_id for order_id in list(set((order1 + order2 + order3 + order4)))]

    # 过滤ID
    hlist = houses.filter(House.id.notin_(order_info_list)).all()

    # 序列化订单信息
    house_info = [house.to_dict() for house in hlist]

    # 返回序列化信息
    return jsonify({'code': '200', 'msg': house_info})


# 排序
@aj_order.route('/sort_search_info/', methods=['GET'])
def sort_search_info():
    # 获取标识
    flag = request.args.get('flag')
    # 筛选房源
    houses = House.query.filter(House.user_id != session.get('user_id'))

    # 最新房源信息
    if flag == '0':
        house_infos = [house.to_dict() for house in houses.order_by(House.id.desc())]
        return jsonify({'code': '200', 'msg': house_infos})

    # 最热房源信息
    elif flag == '1':
        house_infos = [house.to_dict() for house in houses.order_by(House.order_count.desc())]
        return jsonify({'code': '200', 'msg': house_infos})

    # 最性价比房源信息
    elif flag == '2':
        house_infos = [house.to_dict() for house in houses.order_by(House.price.asc())]
        return jsonify({'code': '200', 'msg': house_infos})

    # 最没性价比房源信息
    elif flag == '3':
        house_infos = [house.to_dict() for house in houses.order_by(House.price.desc())]
        return jsonify({'code': '200', 'msg': house_infos})


# 区域名更新
@aj_order.route('/house_name/', methods=['POST'])
def house_name():
    aid = request.args.get('aid')
    aname = Area.query.filter(Area.id == aid).first().name
    return jsonify({'code': '200', 'msg': aname})
