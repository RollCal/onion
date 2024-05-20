from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import F, Q

from reports.models import Report
from .models import Onion, OnionVersus
from .serializers import OnionSerializer, OnionVersusSerializer, OnionDetailSerializer, OVListSerializer
from django.utils import timezone

order_query_dict = {
    "latest": "-created_at",
    "old": "created_at",
}

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

    def get(self, request, onion_id):
        onion = get_object_or_404(Onion, id=onion_id)
        onion_serializer = OnionDetailSerializer(onion)

        onion.num_of_views = F('num_of_views') + 1
        onion.save()
        onion.refresh_from_db()

        return Response(onion_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, onion_id):
        parent_onion = get_object_or_404(Onion, pk=onion_id)
        serializer = OnionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(writer=request.user, parent_onion=parent_onion)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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
            Report.objects.create(
                writer=request.user,
                report_type='UPDATE',
                report_content=request.data,
                content_object=onion
            )

            response = {
                'code': status.HTTP_201_CREATED,
                'message': 'REPORT SEND SUCCESSFULLY',
                'data': request.data,
            }

            return Response(response, status=status.HTTP_201_CREATED)

    def delete(self, request, onion_id):
        onion = get_object_or_404(Onion, id=onion_id)
        # 권한별 로직 분리
        if request.user.is_superuser:
            onion.delete()
            return Response(
                {
                    'code': status.HTTP_200_OK,
                    'message': 'PIE DELETE SUCCESSFULLY',
                }
                , status=status.HTTP_200_OK
            )
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
            ov_instance = get_object_or_404(OnionVersus, Q(orange_onion=onion) | Q(purple_onion=onion))
            ov_instance.orange_onion.delete()
            ov_instance.purple_onion.delete()
            return Response(
                {
                    'code': status.HTTP_200_OK,
                    'message': 'ONION DELETE SUCCESSFULLY',
                }
                , status=status.HTTP_200_OK
            )
        else:
            # 레포트 추가
            Report.objects.create(
                writer=request.user,
                report_type='DELETE',
                report_content=request.data,
                content_object=onion
            )

            response = {
                'code': status.HTTP_201_CREATED,
                'message': 'REPORT SEND SUCCESSFULLY'
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
        # URL에서 ordering 매개변수 가져오기
        ordering = request.query_params.get('ordering', 'latest')  # 기본값은 최신순

        # 최신순 또는 오래된 순으로 양파 가져오기
        try:
            order = order_query_dict[ordering]
        except KeyError:
            order = order_query_dict['latest']
        onionversus = OnionVersus.objects.all().order_by(order)
        ovserializer = OVListSerializer(onionversus, many=True)


        return Response(ovserializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request_data = request.data

        instances = []

        for key, color in zip(request_data, ('Purple', 'Orange')):
            form_data = {
                'title': request_data[key],
                'color': color,
            }

            serializer = OnionSerializer(data=form_data)
            if serializer.is_valid(raise_exception=True):
                instances.append(serializer.save(writer=request.user, parent_onion=None))

        serializer = OnionVersusSerializer(data={
            'purple_onion': instances[0].pk,
            'orange_onion': instances[1].pk,
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
