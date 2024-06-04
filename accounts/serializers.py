from rest_framework import serializers
from .models import User
import re
from datetime import date

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

    # 비밀번호 조건
    def validate_password(self, data):
        if len(data) < 8:
            raise serializers.ValidationError('비밀번호는 최소 8자리여야 합니다.')
        if not re.search(r"[A-Za-z]", data):
            raise serializers.ValidationError('비밀번호에는 최소 하나의 영문이 포함되어야 합니다.')
        if not re.search(r"[0-9!@#$%^&*()_+=-]", data):
            raise serializers.ValidationError('비밀번호에는 최소 하나의 숫자 혹은 특수 문자(!@#$%^&*()_+=-)가 포함되어야 합니다.')
        return data

    # 생년월일 확인
    def validate_birth(self, data):
        if (data < date(1900, 1, 1)) or (data > date.today()):
            raise serializers.ValidationError('입력된 생년월일이 정확한지 확인해주세요')
        return data

    # username 글자수 검증
    def validate_username(self, data):
        if len(data) < 4:
            raise serializers.ValidationError('username의 길이는 최소 4글자 이상이어야 합니다')
        return data

    # nickname 글자수 검증
    def validate_nickname(self, data):
        if len(data) < 4:
            raise serializers.ValidationError('nickname의 길이는 최소 4글자 이상이어야 합니다')
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
