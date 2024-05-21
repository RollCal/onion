from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.db.models import F

from pies.models import Pie
from pies.serializers import PieDetailSerializer
from .models import Onion
from .serializers import OnionSerializer, OnionVersusSerializer
from django.utils import timezone

class OpinionView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            pass
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def get(self, request, onion_id):
        onion = get_object_or_404(Onion, id=onion_id)
        onion_serializer = OnionSerializer(onion)

        onion.num_of_views = F('num_of_views') + 1
        onion.save()
        onion.refresh_from_db()

        content_type = ContentType.objects.get_for_model(onion)
        pies = Pie.objects.filter(content_type=content_type, object_id=onion_id)
        pie_serializer = PieDetailSerializer(pies, many=True)

        response_data = {
            'onion': onion_serializer.data,
            'pies': pie_serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        request_data = request.data

        instances = []

        for key in request_data:
            form_data = {
                'title': request_data[key],
                'writer': request.user.pk,
            }

            serializer = OnionSerializer(data=form_data)
            if serializer.is_valid(raise_exception=True):
                instances.append(serializer.save())

        serializer = OnionVersusSerializer(data={
            'purple_onion': instances[0].pk,
            'orange_onion': instances[1].pk,
        })

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

    def put(self, request, onion_id):
        pass

    def delete(self, request, onion_id):
        pass


class OpinionListView(APIView):

    def get(self, request):
        # URL에서 ordering 매개변수 가져오기
        ordering = request.query_params.get('ordering', 'latest')  # 기본값은 최신순

        onions_data = []

        # 최신순 또는 오래된 순으로 양파 가져오기
        if ordering == 'latest':
            onions = Onion.objects.order_by('-created_at')
        elif ordering == 'oldest':
            onions = Onion.objects.order_by('created_at')
        else:
            onions = Onion.objects.all()

        # 양파를 한 쌍씩 가져와 처리
        for i in range(0, len(onions), 2):
            odd_onion = onions[i]
            even_onion = onions[i + 1]

            # 양파 쌍의 조회수 가져오기
            total_views = odd_onion.num_of_views + even_onion.num_of_views

            # 양파의 제목, 총 조회수 및 생성일 포맷팅
            odd_created_at = self.format_datetime(odd_onion.created_at)

            onion_pair = f"{odd_onion.title} vs {even_onion.title} ({total_views}, {odd_created_at})"
            onions_data.append(onion_pair)

        return Response({'data': onions_data}, status=status.HTTP_200_OK)

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
