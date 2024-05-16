from rest_framework import serializers
from django.contrib.auth import get_user_model

class ProfileSerializer(serializers.ModelSerializer):
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
                  ]
        read_only_fields = ['id',
                            'username',
                            'nickname',
                            'email',
                            'gender',
                            'birth',
                            'karma',
                            'date_joined',
                            ]
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password')
        return ret