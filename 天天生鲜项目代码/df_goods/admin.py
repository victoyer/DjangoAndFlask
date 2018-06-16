from django.contrib import admin
from df_goods.models import GoodsType, Goods, GoodsWheel


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'typename']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id', 'gname', 'gimg', 'gprice', 'gunit', 'gdescribe', 'gtype', 'gstock', 'gclick', 'is_Delete']
    search_fields = ['gname', 'gtype']
    list_filter = ['is_Delete']


class WheelInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['img', 'name', 'trackid']


admin.site.register(GoodsType, TypeInfoAdmin)
admin.site.register(Goods, GoodsInfoAdmin)
admin.site.register(GoodsWheel, WheelInfoAdmin)
