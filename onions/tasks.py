import os
from datetime import date, timedelta
from email.mime.image import MIMEImage

from celery import shared_task
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.db.models import Count
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from votes.models import Vote
from onions.models import OnionViews, OnionVersus

from OpinionProject import settings

cache_key = "highlight"
topics = ["vote", "view"]
generations = [(1, 20), (21, 40), (41, 60), (61, 80), (81, 100)]
genders = ["M", "F"]

html_file = {
    "highlight": ["highlight_form.html",
                "[Opinion] 축하드립니다: 귀하의 어니언이 하이라이트 되었습니다."],
    "confirm": ["confirm_form.html",
                  "[Opinion] 회원가입: 이메일 인증 코드를 입력해주세요."],
}

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
    filtered_onion_versus = []

    for onion_versus_instance in onion_versus:
        orange = target_onion_dict.get(onion_versus_instance.orange_onion.id, 0)
        purple = target_onion_dict.get(onion_versus_instance.purple_onion.id, 0)
        total = orange + purple
        if total >= 3:
            onion_versus_instance.total = total
            filtered_onion_versus.append(onion_versus_instance)

    if not filtered_onion_versus:
        return None
    most_onion_versus = sorted(filtered_onion_versus, key=lambda x: x.total, reverse=True)[0]
    return most_onion_versus.id

def format_label(topic, identifier):
    identifier_map = {
        (1, 20): "청소년이 많이 ",
        (21, 40): "청년이 많이 ",
        (41, 60): "중년이 많이 ",
        (61, 80): "장년이 많이 ",
        (81, 100): "노년이 많이 ",
        "M": "남자가 제일 많이 ",
        "F": "여자가 제일 많이 ",
    }
    topic_map = {
        "view": "본, ",
        "vote": "투표한, ",
    }
    label = ""
    label += identifier_map.get(identifier, "알 수 없는 ")
    label += topic_map.get(topic, " ")
    return label

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

            if highlighted_id is None:
                continue

            label = format_label(topic, generation)

            if highlighted_id in highlight:
                highlight[highlighted_id].append(label)
            else:
                highlight[highlighted_id] = [label]
                highlight["highlighted_ids"].append(highlighted_id)

        for gender in genders:
            highlighted_id = get_statistics(
                    topic=topic,
                    target_type="gender",
                    target_range=gender)

            if highlighted_id is None:
                continue

            label = format_label(topic, gender)

            if highlighted_id in highlight:
                highlight[highlighted_id].append(label)
            else:
                highlight[highlighted_id] = [label]
                highlight["highlighted_ids"].append(highlighted_id)

    if cache.get(cache_key) is not None:
        prev_highlighted_ids = cache.get(cache_key)["highlighted_ids"]
    else:
        prev_highlighted_ids = []

    for h_id in highlight["highlighted_ids"]:
        highlight[h_id][-1] = highlight[h_id][-1][:-2]
        if h_id not in prev_highlighted_ids:

            ov = OnionVersus.objects.get(id=h_id)
            send_alert(
                type="highlight",
                to_email=ov.purple_onion.writer.email,
                data={
                    "message": ov.ov_title,
                    "username": ov.purple_onion.writer.nickname
                }
            )

    cache.set(cache_key, highlight, 60*60)

@shared_task
def send_alert(type, to_email, data):
    form_file, subject = html_file[type]

    html_content = render_to_string(form_file, data)

    email = EmailMessage(
        subject,
        html_content,
        'no-reply@onion-pi.com',
        [to_email],
    )
    email.content_subtype = 'html'

    image_path = os.path.join(settings.BASE_DIR, 'onions', 'data_management', 'templates', 'opinion-logo.jpg')

    with open(image_path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', '<image1>')
        img.add_header('Content-Disposition', 'inline', filename='onion-logo.jpg')
        email.attach(img)

    email.send()
