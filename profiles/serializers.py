from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from pies.models import Pie
from onions.models import Onion
from votes.models import Vote

# profile에서 사용할 pie serializer
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

# profile에서 사용할 투표한 onion serializer
class ProfileVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Onion
        fields = [
            'title',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'title',
            'created_at',
            'updated_at',
        ]

class ProfileSerializer(serializers.ModelSerializer):
    pie_set = ProfilePieSerializer(many=True, read_only=True)
    voted_onions = serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'password',
            'nickname',
            'email',
            'gender',
            'birth',
            'karma',
            'date_joined',
            'pie_set',
            'voted_onions',
            ]
        read_only_fields = [
            'id',
            'username',
            'nickname',
            'email',
            'gender',
            'birth',
            'karma',
            'date_joined',
            'pie_set',
            'voted_onions',
            ]
    #비밀번호 제외
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password')
        return ret

    def get_voted_onions(self, instance):
        # Vote 모델에서 사용자와 연결된 Onion 객체 가져오기
        content_type = ContentType.objects.get_for_model(Onion)
        votes = Vote.objects.filter(user=instance, content_type=content_type)
        onions = Onion.objects.filter(id__in=votes.values_list('object_id', flat=True))
        return ProfileVoteSerializer(onions, many=True).data