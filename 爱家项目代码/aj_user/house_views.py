from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
import os
from aj_user.models import Area, Facility, House, HouseImage
from utils import status_code
from aj_user.models import db
from utils.setting import UPLOAD_DIR
from utils.ModFilter import is_login

aj_house = Blueprint('house', __name__)


# 访问我的房源
@aj_house.route('/myhouse/', methods=['GET'])
@is_login
def myhouse():
    return render_template('myhouse.html')


# 查看所有已发布房源信息
@aj_house.route('/house_info/', methods=['GET'])
@is_login
def house_info():
    # 查询当前用户所有已发布房源信息
    house_all_info = House.query.filter_by(user_id=session.get('user_id')).all()
    # 定义一个列表序列化返回信息
    house_all_info_list = [house.to_dict() for house in house_all_info]
    return jsonify({'code': '200', 'data': house_all_info_list})


# 访问添加房源
@aj_house.route('/newhouse/', methods=['GET'])
@is_login
def newhouse():
    return render_template('newhouse.html')


# # 访问添加房源信息页面
@aj_house.route('/area_facility/', methods=['GET'])
@is_login
def area_facility():
    # 获取Area和Facility的详细信息
    area_alls = Area.query.all()
    facility_all = Facility.query.all()
    # 定义序列化JSON格式数据的列表
    area_list = [area.to_dict() for area in area_alls]
    facility_list = [faility.to_dict() for faility in facility_all]
    # 返回序列化结果
    return jsonify({'code': '200', 'msg': area_list, 'data': facility_list})


# 创建新房源信息
@aj_house.route('/newhouse/', methods=['POST'])
@is_login
def newhouse_info():
    # 接收数据
    data_all = request.form.to_dict()
    facility_ids = request.form.getlist('facility')

    # 获取创建对象的数据

    house = House()
    house.user_id = session.get('user_id')
    house.area_id = data_all['area_id']
    house.title = data_all['title']
    house.price = data_all['price']
    house.address = data_all['address']
    house.room_count = data_all['room_count']
    house.acreage = data_all['acreage']
    house.unit = data_all['unit']
    house.capacity = data_all['capacity']
    house.beds = data_all['beds']
    house.deposit = data_all['deposit']
    house.min_days = data_all['min_days']
    house.max_days = data_all['max_days']

    # 根据设施号查询所有对应的设施对象
    if facility_ids:
        # 在house创建facilities记录并保存
        house.facilities = Facility.query.filter(Facility.id.in_(facility_ids)).all()

    # 保存
    try:
        house.add_update()
    except:
        db.session.rollback()

    return jsonify({'code': 200, 'house_id': house.id})


# 保存新房源图片
@aj_house.route('/house_image/', methods=['POST'])
@is_login
def house_image():
    # 获取提交表单信息
    house_id = request.form.get('house_id')
    house_img = request.files.get('house_image')

    # 保存图片的绝对路径
    img_path_full = os.path.join(UPLOAD_DIR, house_img.filename)

    # 保存图片相对路径
    img_path = os.path.join('img', house_img.filename)

    # 保存图片到本地
    house_img.save(img_path_full)

    # 保存首张图片
    house = House.query.get(house_id)
    if not house.index_image_url:
        house.index_image_url = img_path

    # 保存图片到数据库
    house_img = HouseImage()
    house_img.house_id = house_id
    house_img.url = img_path
    try:
        house_img.add_update()

    except:
        db.session.rollback()
        return jsonify(status_code.USER_UPDATE_MYSQL_NO)

    return jsonify({'code': '200', 'img': img_path})


# 房屋详情
@aj_house.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


# 房屋信息
@aj_house.route('/detail/<int:id>/', methods=['GET'])
def house_detail(id):
    house = House.query.get(id)
    house_info = house.to_full_dict()

    return jsonify({'code': '200', 'msg': house_info})


# 即刻预约
@aj_house.route('/booking/', methods=['GET'])
def booking():
    return render_template('booking.html')
