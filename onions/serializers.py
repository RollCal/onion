from collections import deque
from itertools import chain

from django.db.models import Count
from rest_framework import serializers
from onions.models import Onion, OnionVersus
from django.shortcuts import get_object_or_404

class OnionSerializer(serializers.ModelSerializer):

    up_vote_num = serializers.SerializerMethodField()
    down_vote_num = serializers.SerializerMethodField()

    class Meta:
        model = Onion
        fields = '__all__'
        read_only_fields = ('writer',
                            'parent_onion',
                            'color',
                            'num_of_views',
                            'created_at',
                            'updated_at')

    def get_up_vote_num(self, obj):
        return obj.votes.filter(type='Up').count()

    def get_down_vote_num(self, obj):
        return obj.votes.filter(type='Down').count()

class OnionDetailSerializer(OnionSerializer):

    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        children = obj.child_onions.all()
        return OnionDetailSerializer(children, many=True).data

class OnionVisualizeSerializer(OnionSerializer):

    next = serializers.SerializerMethodField()

    def get_next(self, obj):
        children = obj.child_onions.annotate(children_votes_count=Count('votes')).order_by('-children_votes_count')
        if children.exists():
            next_child = children[0]
            return OnionVisualizeSerializer(next_child).data


class OnionVersusSerializer(serializers.ModelSerializer):

    class Meta:
        model = OnionVersus
        fields = '__all__'

class OVListSerializer(OnionVersusSerializer):
    orange_onion = serializers.SerializerMethodField()
    purple_onion = serializers.SerializerMethodField()

    def get_orange_onion(self, obj):
        orange_ins = get_object_or_404(Onion, pk=obj.orange_onion_id)
        return OnionSerializer(orange_ins).data

    def get_purple_onion(self, obj):
        purple_ins = get_object_or_404(Onion, pk=obj.purple_onion_id)
        return OnionSerializer(purple_ins).data
