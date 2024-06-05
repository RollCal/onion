from collections import deque
from itertools import chain

from django.core.cache import cache
from django.db.models import Count
from rest_framework import serializers
from onions.models import Onion, OnionVersus
from django.shortcuts import get_object_or_404

class OnionSerializer(serializers.ModelSerializer):

    up_vote_num = serializers.SerializerMethodField()
    down_vote_num = serializers.SerializerMethodField()
    voted = serializers.SerializerMethodField()

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

    def get_voted(self, obj):
        if self.context =={}:
            return None
        voted = obj.votes.filter(
            user=self.context
        )
        if voted.exists():
            return voted[0].type
        else:
            return None

class OnionDetailSerializer(OnionSerializer):

    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        children = obj.child_onions.all()
        return OnionDetailSerializer(children, context=self.context, many=True).data

class OnionVisualizeSerializer(OnionSerializer):

    next = serializers.SerializerMethodField()

    def get_next(self, obj):
        children = obj.child_onions.annotate(children_votes_count=Count('votes')).order_by('-children_votes_count')
        if children.exists():
            next_child = children[0]
            return OnionSerializer(next_child).data


class OnionVersusSerializer(serializers.ModelSerializer):

    class Meta:
        model = OnionVersus
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('title_embedding', None)
        data.pop('purple_embedding', None)
        data.pop('orange_embedding', None)
        return data

class OVListSerializer(OnionVersusSerializer):
    orange_onion = serializers.SerializerMethodField()
    purple_onion = serializers.SerializerMethodField()
    highlight = serializers.SerializerMethodField()

    def get_orange_onion(self, obj):
        orange_ins = get_object_or_404(Onion, pk=obj.orange_onion_id)
        return OnionVisualizeSerializer(orange_ins).data

    def get_purple_onion(self, obj):
        purple_ins = get_object_or_404(Onion, pk=obj.purple_onion_id)
        return OnionVisualizeSerializer(purple_ins).data

    def get_highlight(self, obj):

        if not cache.get("highlight"):
            return None

        highlight = cache.get("highlight")
        if obj.id in highlight["highlighted_ids"]:
            return highlight[obj.id]
        else:
            return None
