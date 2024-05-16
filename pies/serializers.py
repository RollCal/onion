from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Pie


class PieSerializer(serializers.ModelSerializer):
    content_type = serializers.ReadOnlyField(source='content_type.model')
    writer = serializers.ReadOnlyField(source='writer.username')

    class Meta:
        model = Pie
        fields = [
            'id',
            'content_type',
            'object_id',
            'color',
            'title',
            'writer',
            'num_of_views',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['object_id']


class PieDetailSerializer(PieSerializer):

    class Meta(PieSerializer.Meta):
        # 가져온 Serializer에서 필드 추가
        fields = PieSerializer.Meta.fields + ['pies']

    # 메서드에서 pies 가져오기
    pies = serializers.SerializerMethodField()

    # pie에 달린 pies 가져오기
    def get_pies(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        pies = Pie.objects.filter(content_type=content_type, object_id=obj.id)
        pies_serializer = self.__class__(pies, many=True)
        return pies_serializer.data
