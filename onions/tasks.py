from datetime import date, timedelta
from celery import shared_task
from django.core.cache import cache
from django.db.models import Count

from votes.models import Vote
from onions.models import OnionViews, OnionVersus

cache_key = "highlight"
topics = ["vote", "view"]
generations = [(1, 20), (21, 40), (41, 60), (61, 80), (81, 100)]
genders = ["M", "F"]

def get_statistics(topic, target_type, target_range):

    TopicModel = OnionViews if topic=="view" else Vote

    if target_type == "generation":
        today = date.today()
        s = today - timedelta(days=365 * target_range[1])
        e = today - timedelta(days=365 * target_range[0])
        target = TopicModel.objects.filter(user__birth__range=(s, e))
    else:
        target = TopicModel.objects.filter(user__gender=target_range)

    if not target.exists():
        return None

    target_onion = target.values('onion').annotate(target_count=Count('id'))
    target_onion_dict = {t['onion']: t['target_count'] for t in target_onion}
    onion_versus = OnionVersus.objects.all()
    for onion_versus_instance in onion_versus:
        orange = target_onion_dict.get(onion_versus_instance.orange_onion.id, 0)
        purple = target_onion_dict.get(onion_versus_instance.purple_onion.id, 0)
        onion_versus_instance.total = orange + purple
    most_onion_versus = sorted(onion_versus, key=lambda x: x.total, reverse=True)[0]

    return most_onion_versus.id

@shared_task
def upload_highlight():
    highlight = {
        'highlighted_ids': [],
    }

    for topic in topics:
        for generation in generations:

            highlighted_id = get_statistics(
                    topic=topic,
                    target_type="generation",
                    target_range=generation)

            if highlighted_id in highlight:
                highlight[highlighted_id].append(f"{topic}_{generation}")
            else:
                highlight[highlighted_id] = [f"{topic}_{generation}"]
                highlight["highlighted_ids"].append(highlighted_id)

        for gender in genders:
            highlighted_id = get_statistics(
                    topic=topic,
                    target_type="gender",
                    target_range=gender)
            if highlighted_id in highlight:
                highlight[highlighted_id].append(f"{topic}_{gender}")
            else:
                highlight[highlighted_id] = [f"{topic}_{gender}"]
                highlight["highlighted_ids"].append(highlighted_id)

    cache.set(cache_key, highlight, 60*60)
