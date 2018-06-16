from django.db import models


# 商品类型模型类
class GoodsType(models.Model):
    typename = models.CharField(max_length=20, verbose_name='分类名称')  # 分类名称
    isDelete = models.BooleanField(default=False, verbose_name='逻辑删除')  # 逻辑删除

    class Meta:
        db_table = 'df_type'

    def __str__(self):
        return self.typename


# 商品模型类
class Goods(models.Model):
    gname = models.CharField(max_length=30, verbose_name='商品名称')  # 商品名称
    gimg = models.ImageField(upload_to='df_goods', verbose_name='商品图片')  # 商品图片
    gprice = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='商品价格')  # 商品价格(价格一共6位，两位小数)
    gunit = models.CharField(max_length=20, default='500g', verbose_name='商品规格')  # 商品出售规格
    gsort = models.IntegerField(default=0, verbose_name='排序')  # 排序
    gdescribe = models.CharField(max_length=200, verbose_name='商品描述')  # 商品描述
    gtype = models.ForeignKey(GoodsType, verbose_name='商品类型')  # 关联商品类型
    gstock = models.IntegerField(verbose_name='商品库存')  # 商品库存
    gclick = models.IntegerField(verbose_name='商品被点击次数')  # 商品点击次数
    is_Delete = models.BooleanField(default=False, verbose_name='逻辑删除')  # 逻辑删除

    class Meta:
        db_table = 'df_goods'

    def __str__(self):
        return self.gname


# 轮播图
class GoodsWheel(models.Model):
    img = models.ImageField(upload_to='df_goods', verbose_name='轮播图片')
    name = models.CharField(max_length=20, verbose_name='轮播商品名称')
    trackid = models.CharField(max_length=16, verbose_name='通用ID')


def biubiu():
    Goods.objects.create()
