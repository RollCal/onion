from rest_framework import serializers

from onions.models import Onion, OnionVersus

class OnionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Onion
        fields = '__all__'

class OnionVersusSerializer(serializers.ModelSerializer):

    class Meta:
        model = OnionVersus
        fields = '__all__'