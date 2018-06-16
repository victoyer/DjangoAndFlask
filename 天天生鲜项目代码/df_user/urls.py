from django.conf.urls import url
from df_user import views

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'logout', views.logout, name='logout'),
    # url(r'^index/', views.index, name='index'),
    url(r'^verusername/', views.VerUserName, name='VerUserName'),
    url(r'^UserCenterInfo/', views.UserCenterInfo, name='usercenterinfo'),
    url(r'^UserCenterOrder/', views.UserCenterOrder, name='usercenterorder'),
    url(r'^UserCeenterSite/', views.UserCeenterSite, name='usercentersite'),
]
