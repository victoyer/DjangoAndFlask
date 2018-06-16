from rest_framework import serializers
from user.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=32, error_messages={'blank': '用户名不能为空'})

    class Meta:
        model = UserModel
        fields = ['username']

    def update(self, instance, validated_data):
        pass
