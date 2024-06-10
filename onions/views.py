from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from management.models import Report
from .models import Onion, OnionVersus, OnionViews
from .serializers import (OnionSerializer,
                          OnionVersusSerializer,
                          OnionDetailSerializer,
                          OVListSerializer,
                          OnionVisualizeSerializer)
from django.utils import timezone
from .utils import get_embedding, search_words, ov_ordering
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.cache import cache

import time

order_query_dict = {
    "latest": "-created_at",
    "old": "created_at",
    "popular": "popular",
    "relevance": "relevance",
    "recommend": "recommend",
}

@api_view(['GET'])
def onion_visualize(request, pk):
    onion = get_object_or_404(Onion, pk=pk)
    return Response(OnionVisualizeSerializer(onion).data, status=status.HTTP_200_OK)

class OpinionView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            pass
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def update_onion(self, request_data, onion):
        serializer = OnionSerializer(onion, data=request_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'code': status.HTTP_200_OK,
                'message': 'ONION UPDATE SUCCESSFULLY',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def delete_onion(self, onion):
        if onion.parent_onion is None: # 최상위 Onion일 때
            ov_instance = get_object_or_404(OnionVersus, Q(orange_onion=onion) | Q(purple_onion=onion))
            ov_instance.orange_onion.delete()
            ov_instance.purple_onion.delete()
        else:
            onion.delete()

        return Response(
            {
                'code': status.HTTP_200_OK,
                'message': 'ONION DELETE SUCCESSFULLY',
            }
            , status=status.HTTP_200_OK
        )

    def get(self, request, onion_id):
        onion = get_object_or_404(Onion, id=onion_id)

        if request.user.is_authenticated:
            context = {'now_user': request.user}
        else:
            context = {}

        onion_serializer = OnionDetailSerializer(onion, context=context)

        onion.num_of_views = F('num_of_views') + 1
        onion.save()
        onion.refresh_from_db()

        if onion.parent_onion is None and request.user.is_authenticated:
            OnionViews.objects.get_or_create(onion=onion, user=request.user)

        return Response(onion_serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic()
    def post(self, request, onion_id):
        request_data = request.data

        parent_onion = get_object_or_404(Onion, pk=onion_id)
        serializer = OnionSerializer(data=request_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(color=request_data['color'], writer=request.user, parent_onion=parent_onion)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic()
    def put(self, request, onion_id):
        onion = get_object_or_404(Onion, id=onion_id)

        # 슈퍼계정 일때
        if request.user.is_superuser:
            return self.update_onion(request.data, onion)

        # 일반유저 일때
        if request.user != onion.writer: # 작성자 체크
            return Response(
                {
                    'code': status.HTTP_403_FORBIDDEN,
                    'message': 'Permission denied.'
                }
                , status=status.HTTP_403_FORBIDDEN
            )

        time_difference = timezone.now() - onion.created_at
        if time_difference.total_seconds() <= 300:
            # 직렬화를 사용하여 기존 onion 객체를 업데이트
            return self.update_onion(request.data, onion)
        else:
            # 관리자만 볼수있는 레포트에 추가
            report = Report(
                writer=request.user,
                report_type='UPDATE',
                report_content=request.data,
                content_type=ContentType.objects.get_for_model(Onion),
                content_object=onion
            )
            try:
                report.save()
                code = status.HTTP_201_CREATED
                message = "REPORT SEND SUCCESSFULLY"
            except ValidationError as e:
                code = status.HTTP_400_BAD_REQUEST
                message = "REPORT ALREADY EXISTS"

            response = {
                'code': code,
                'message': message,
                'data': request.data,
            }

            return Response(response, status=status.HTTP_201_CREATED)

    @transaction.atomic()
    def delete(self, request, onion_id):
        onion = get_object_or_404(Onion, id=onion_id)
        # 권한별 로직 분리
        if request.user.is_superuser:
            return self.delete_onion(onion)

        # 작성자 체크
        if request.user != onion.writer:
            return Response(
                {
                    'code': status.HTTP_403_FORBIDDEN,
                    'message': 'Permission denied.'
                }
                , status=status.HTTP_403_FORBIDDEN
            )

        time_difference = timezone.now() - onion.created_at
        if time_difference.total_seconds() <= 300:
            return self.delete_onion(onion)
        else:
            # 레포트 추가
            report = Report(
                writer=request.user,
                report_type='DELETE',
                report_content=request.data,
                content_type=ContentType.objects.get_for_model(Onion),
                content_object=onion
            )
            try:
                report.save()
                code = status.HTTP_201_CREATED
                message = "REPORT SEND SUCCESSFULLY"
            except ValidationError as e:
                code = status.HTTP_400_BAD_REQUEST
                message = "REPORT ALREADY EXISTS"

            response = {
                'code': code,
                'message': message,
                'data': request.data,
            }

            return Response(response, status=status.HTTP_201_CREATED)

class OpinionListView(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
            return super().get_permissions()
        else:
            self.permission_classes = [AllowAny]
            return super().get_permissions()

    def get(self, request):
        ordering = request.GET.get('order')
        page = request.GET.get('page')

        if ordering is None or page is None:
            return Response(data={"error": "'order' or 'page' is empty"}, status=status.HTTP_400_BAD_REQUEST)

        if "search" in ordering:
            search = ordering.split(":")[-1].strip()
            ordering = "relevance"
        else:
            search = None

        try:
            ordering = order_query_dict[ordering]
        except KeyError:
            ordering = order_query_dict['latest']

        onionversus = OnionVersus.objects.all()
        cached = False

        if ordering == "relevance":
            onionversus = search_words(search)
        else:
            onionversus_cached = cache.get(ordering, None)
            if onionversus_cached is None:
                cached = True
                onionversus = ov_ordering(onionversus, ordering)
                cache.set(ordering, onionversus, timeout=30)
            else:
                onionversus = onionversus_cached

        paginator = Paginator(onionversus, 3)

        try:
            onionversus = paginator.page(page)
        except PageNotAnInteger:
            onionversus = paginator.page(1)
        except EmptyPage:
            onionversus = paginator.page(paginator.num_pages)

        ovserializer = OVListSerializer(onionversus, many=True)

        return Response({
            "meta": {
                "now_page": page,
                "num_page": paginator.num_pages,
                "ordering": ordering,
                "cached": cached,
            },
            "data": ovserializer.data,
        }, status=status.HTTP_200_OK)


    @transaction.atomic()
    def post(self, request):
        request_data = request.data
        ov_title, purple_title, orange_title = (request_data['title'],
                                                request_data['purple_title'],
                                                request_data['orange_title'])

        purple_serializer = OnionSerializer(data={
            'title': purple_title,
        })
        orange_serializer = OnionSerializer(data={
            'title': orange_title,
        })

        if purple_serializer.is_valid(raise_exception=True) and \
                orange_serializer.is_valid(raise_exception=True):

            embeddings = get_embedding([ov_title, purple_title, orange_title])

            purple_ins = purple_serializer.save(color="Purple", writer=request.user, parent_onion=None)
            orange_ins = orange_serializer.save(color="Orange", writer=request.user, parent_onion=None)

            serializer = OnionVersusSerializer(data={
                'ov_title': ov_title,
                'purple_onion': purple_ins.pk,
                'orange_onion': orange_ins.pk,
                'title_embedding': [] if embeddings is None else embeddings[ov_title],
                'purple_embedding': [] if embeddings is None else embeddings[purple_title],
                'orange_embedding': [] if embeddings is None else embeddings[orange_title],
            })

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

    def format_datetime(self, dt):
        # 현재 시간 구하기
        now = timezone.now()

        # 시간차 계산
        delta = now - dt

        # 주, 일, 시간 전부터 표시
        if delta.days > 6:
            weeks = int(delta.days / 7)
            return f"{weeks}주 전"
        elif delta.days > 0:
            return f"{delta.days}일 전"
        else:
            hours = int(delta.seconds / 3600)
            if hours > 0:
                return f"{hours}시간 전"
            else:
                minutes = int(delta.seconds / 60)
                if minutes > 0:
                    return f"{minutes}분 전"
                else:
                    return "방금 전"
