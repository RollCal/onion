from rest_framework import serializers
from django.contrib.auth import get_user_model
from pies.models import Pie

class ProfilePieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pie
        fields = [
            'id',
            'object_id',
            'color',
            'title',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'object_id',
            'color',
            'title',
            'created_at',
            'updated_at',
        ]
class ProfileSerializer(serializers.ModelSerializer):
    pie_set = ProfilePieSerializer(many=True, read_only=True)
    class Meta:
        model = get_user_model()
        fields = ['id',
                  'username',
                  'password',
                  'nickname',
                  'email',
                  'gender',
                  'birth',
                  'karma',
                  'date_joined',
                  'pie_set',
                  ]
        read_only_fields = ['id',
                            'username',
                            'nickname',
                            'email',
                            'gender',
                            'birth',
                            'karma',
                            'date_joined',
                            'pie_set',
                            ]
    #비밀번호 제외
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password')
        return ret