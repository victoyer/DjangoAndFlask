from django.db import models


class CartInfoManage(models.Manager):
    def create_cart(self, uid, gid, count):
        cart = self.create(user_id=uid, goods_id=gid, count=count)
        return cart


# 购物车模型类
class CartInfo(models.Model):
    user = models.ForeignKey('df_user.UserInfo')  # 关联用户
    goods = models.ForeignKey('df_goods.Goods')  # 关联商品
    count = models.IntegerField()  # 购物车商品数量

    class Meat:
        db_table = 'df_cart'

    objects = CartInfoManage()
