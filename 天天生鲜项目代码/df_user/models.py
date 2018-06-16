from django.db import models


# 用户信息模型类
class UserInfo(models.Model):
    uname = models.CharField(max_length=20, unique=True)  # 用户名
    upwd = models.CharField(max_length=100)  # 用户密码
    uemail = models.CharField(max_length=30, unique=True)  # 用户邮箱

    class Meta:
        db_table = 'df_user'


# 收件人信息模型类
class AddressInfo(models.Model):
    ushou = models.CharField(max_length=20)  # 收件人姓名
    uaddress = models.CharField(max_length=100)  # 收件人地址
    uzipcode = models.CharField(max_length=6)  # 收件人邮编
    uphone = models.CharField(max_length=11, unique=True)  # 收件人手机号

    class Meta:
        db_table = 'df_addr'


# 用户ticket储存模型类
class UserTicket(models.Model):
    user = models.ForeignKey(UserInfo)  # 关联用户
    ticket = models.CharField(max_length=33)  # 用户登录时生成的ticket
    out_time = models.DateTimeField()  # 用户ticket过期时间

    class Meta:
        db_table = 'df_ticket'
