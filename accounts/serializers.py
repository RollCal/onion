from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password2',
            'nickname',
            'email',
            'gender',
            'birth',
            'karma',
            'last_login',
            'date_joined',
            'is_superuser',
            'is_staff',
            'is_active',
        ]
        read_only_fields = (
            'karma',
            'date_joined',
            'last_login',
            'is_superuser',
            'is_staff',
            'is_active',
        )

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Passwords don't match"}
            )

        data.pop('password2')
        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            email=validated_data['email'],
            gender=validated_data['gender'],
            birth=validated_data['birth'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
