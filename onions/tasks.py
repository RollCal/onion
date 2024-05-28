import datetime

from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Case, When, ExpressionWrapper, F, IntegerField, Count, DateField
from django.db.models.functions import Now, Cast, ExtractYear

from OpinionProject import settings
from django.core.cache import cache

from votes.models import Vote
from onions.models import OnionViews

cache_key = "highlight"
topics = ["upvote", "downvote", "view"]
generations = [(1, 20), (21, 40), (41, 60), (61, 80), (81, 100)]
genders = ["M", "F"]

def get_target(topic):
    if topic in ["upvote", "downvote"]:
        return Vote.objects.select_related(
            "user",
            "onion"
        ).filter(
            onion__parent_onion_id=None
        )
    elif topic in ["view"]:
        return OnionViews.objects.select_related(
            "user",
            "onion"
        ).filter(
            onion__parent_onion_id=None
        )
    else:
        return Vote.objects

def get_generation_topic(topic, generation):

    target = get_target(topic)

    highlight = target.annotate(
        age=ExpressionWrapper(
            ExtractYear(Now())-ExtractYear('user__birth'),
            output_field=IntegerField()
        )
    ).filter(
        age__gte=generation[0],
        age__lte=generation[1]
    ).values('onion_id').annotate(
        count=Count('onion_id')
    ).order_by('-count').first()

    return highlight

def get_gender_topic(topic, gender):

    target = get_target(topic)

    highlight = target.filter(
        user__gender=gender
    ).values('onion_id').annotate(
        count=Count('onion_id')
    ).order_by('-count').first()

    return highlight

@shared_task
def upload_highlight():
    highlight = {}

    for topic in topics:
        highlight[topic] = {}
        for generation in generations:
            highlight[topic][f'{generation[0]}_to_{generation[1]}'] = get_generation_topic(topic, generation)

        for gender in genders:
            highlight[topic][f'{gender}'] = get_gender_topic(topic, gender)

    print(highlight)
    #cache.set(cache_key, highlight, 10)

