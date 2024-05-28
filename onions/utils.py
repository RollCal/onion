from OpinionProject import settings
import requests
from django.db.models.functions import Least, Coalesce
from django.db.models import Sum, Subquery, OuterRef, F
from pgvector.django import L2Distance
from onions.models import OnionVersus
from votes.models import Vote


def get_embedding(words):
    request_data = {
        "words": words
    }

    response = requests.post(settings.EMBEDDING_HOST, json=request_data)

    if response.status_code == 200:
        embeddings = response.json().get('embeddings')
    else:
        embeddings = None

    return embeddings

def search_words(search):

    embeddings = get_embedding(search)[search]

    onionversus = OnionVersus.objects.annotate(
        max_distance=Least(
            L2Distance('title_embedding', embeddings),
            L2Distance('purple_embedding', embeddings),
            L2Distance('orange_embedding', embeddings),
        )
    ).order_by('max_distance')

    return onionversus

def ov_ordering(ovlist, order):
    if order == "relevance":
        return ovlist
    elif order == "popular":
        orange_votes = Vote.objects.filter(
            onion_id=OuterRef('orange_onion')
        ).values('onion__id').annotate(
            total=Sum('id')
        ).values('total')

        purple_votes = Vote.objects.filter(
            onion_id=OuterRef('purple_onion')
        ).values('onion__id').annotate(
            total=Sum('id')
        ).values('total')

        return ovlist.annotate(
            total_orange_votes=Coalesce(Subquery(orange_votes), 0),
            total_purple_votes=Coalesce(Subquery(purple_votes), 0)
        ).annotate(
            total_votes=Sum(F('total_orange_votes') + F('total_purple_votes'))
        ).order_by('-total_votes')

    elif order == "recommend":
        return ovlist
    else:
        return ovlist.order_by(order)
