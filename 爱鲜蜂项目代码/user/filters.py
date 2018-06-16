import django_filters
from rest_framework import filters
from user.models import UserModel


class UserFilter(filters.FilterSet):
    username = django_filters.CharFilter('username', lookup_expr='contains')

    class Meta:
        model = UserModel
        fields = ['username']
