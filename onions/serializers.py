from rest_framework import serializers

from onions.models import Onion, OnionVersus

class OnionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Onion
        fields = '__all__'
        read_only_fields = ('writer',
                            'num_of_views',
                            'created_at',
                            'updated_at')

class OnionVersusSerializer(serializers.ModelSerializer):

    class Meta:
        model = OnionVersus
        fields = '__all__'