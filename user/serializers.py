from rest_framework import serializers
from .models import MyUser


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "can_be_contacted",
            "can_data_be_shared",
        ]
        read_only_fields = [
            "id",
            "date_joined",
            "is_superuser",
            "last_login",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        ]
