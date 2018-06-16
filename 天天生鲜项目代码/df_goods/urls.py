from django.conf.urls import url
from df_goods import views

urlpatterns = [
    url(r'^cart/', views.cart, name='cart'),
    # url(r'^detail/', views.detail, name='detail'),
    # url(r'^list/$', views.list, name='list'),
    url(r'^list(\d+)_(\d+)_(\d+)/', views.list, name='list'),
    url(r'^placeOrder/', views.placeOrder, name='placeOrder'),
    url(r'^index/', views.index, name='index'),
    url(r'^detail/(\d+)/', views.detail, name='detail'),
    url(r'^info/', views.info, name='info')
]
