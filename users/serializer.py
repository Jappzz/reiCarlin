
from rest_framework import serializers
from reiCarlin.users.models import User
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    is_employee = serializers.BooleanField(default=False)
    is_superUser = serializers.BooleanField(default=False)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email already exists.")
        return value
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Username already exists.")
        return value
    def create(self, validated_data):
        if validated_data["is_employee"] is False:
          user = User.objects.create_user(**validated_data)  
        else:
            user = User.objects.create_superuser(**validated_data)
        return user
    def update(self, instance: User, validated_data: dict):
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)