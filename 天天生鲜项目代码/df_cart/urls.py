from django.conf.urls import url
from df_cart import views

urlpatterns = [
    url(r'^index/', views.cart, name='index'),
    url(r'^addcart(\d+)_(\d+)/', views.addcart, name='addcart')
]
