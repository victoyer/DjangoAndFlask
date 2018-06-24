OK = 200

# 用户模块
USER_REGISTER_DATA_NOT_NULL = {'code': '1001', 'msg': '请将注册信息填写完整!'}
USER_REGISTER_MOBILE_ERROR = {'code': '1002', 'msg': '手机号不正确!'}
USER_REGISTER_PASSWORD_IS_NOT_VALID = {'code': '1003', 'msg': '两次输入密码不一致!'}
USER_REGISTER_MOBILE_EXISTS = {'code': '1004', 'msg': '该用户已注册，请直接登录!'}

SUCCESS = {'code': '200', 'msg': '请求成功!'}

USER_LOGIN_DATA_NOT_NULL = {'code': '1005', 'msg': '请将登录信息填写完整!'}
USER_LOGIN_USER_NOT_EXISTS = {'code': '1006', 'msg': '用户名错误或未注册!'}
USER_LOGIN_PASSWORD_IS_NOT_VALID = {'code': '1007', 'msg': '密码错误!'}

USER_CHANGE_PROFILE_IMAGE = {'code': '1008', 'msg': '上传文件不是图片！'}

DATABASEERROR = {'code': '0', 'msg': '数据库错误！'}

USER_UPDATE_NAME_IDENTICAL = {'code': '1009', 'msg': '用户名没有更改'}
USER_UPDATE_NAME_EXISTENCE = {'code': '1010', 'msg': '用户名已存在'}
USER_UPDATE_MYSQL_NO = {'code': '1011', 'msg': '服务器繁忙请稍后重试！'}

USER_AUTH_IS_NOT_NULL = {'code': '1012', 'msg': '请填写完整的实名认证信息！'}
USER_AUTH_ID_CARD_IS_NOT_VALID = {'code': '1013', 'msg': '请填写正确的身份证号'}

HOUSE_DATA_IS_NOT_NULL = {'code': '1014', 'msg': '请将房源信息填写完整'}

# 订单模块
ORDER_DATA_IS_NOT_NULL = {'code': '1100', 'msg': '请将订单信息填写完整'}
ORDER_DATA_DATETIME_ERROR = {'code': '1101', 'msg': '住房起始时间大于结束时间'}

