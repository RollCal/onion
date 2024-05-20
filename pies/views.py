from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import PieSerializer, PieDetailSerializer
from onions.models import Onion
from .models import Pie
from django.db.models import F
from reports.models import Report


class PiesAPIView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            pass
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    # pie 목록 조회
    def get(self, request, pie_id):
        pie = get_object_or_404(Pie, id=pie_id)

        pie.num_of_views = F('num_of_views') + 1
        pie.save()
        pie.refresh_from_db()

        pies_serializer = PieDetailSerializer(pie)

        return Response(pies_serializer.data, status=status.HTTP_200_OK)

    # pie 등록
    def post(self, request):

        # content_type 체크
        if 'content_type' not in request.data:
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'content_type is required'
                }
                , status=status.HTTP_400_BAD_REQUEST
            )

        # id 체크
        if 'id' not in request.data:
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'id is required'
                }
                , status=status.HTTP_400_BAD_REQUEST
            )

        # Pie 의 pie
        if request.data['content_type'] == 'pie':
            obj = get_object_or_404(Pie, id=request.data['id'])
        # onion 의 pie
        elif request.data['content_type'] == 'onion':
            obj = get_object_or_404(Onion, id=request.data['id'])
        else:
            return Response(
                {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Unsupported content type',
                }
                , status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(writer=request.user, content_object=obj)
            response = {
                'code': status.HTTP_201_CREATED,
                'message': 'PIE CREATED SUCCESSFULLY',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request, pie_id):
        pie = get_object_or_404(Pie, id=pie_id)

        # 권한별 로직 분리
        #
        # 슈퍼계정 일때

        if request.user.is_superuser:
            serializer = PieSerializer(pie, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = {
                    'code': status.HTTP_200_OK,
                    'message': 'PIE UPDATE SUCCESSFULLY',
                    'data': serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)

        # 일반유저 일때
        else:

            # 작성자 체크
            if request.user != pie.writer:
                return Response(
                    {
                        'code': status.HTTP_403_FORBIDDEN,
                        'message': 'Permission denied.'
                    }
                    , status=status.HTTP_403_FORBIDDEN
                )

            # 관리자만 볼수있는 레포트에 추가
            Report.objects.create(
                writer=request.user,
                report_type='UPDATE',
                report_content=request.data,
                content_object=pie
            )

            response = {
                'code': status.HTTP_201_CREATED,
                'message': 'REPORT SEND SUCCESSFULLY',
                'data': request.data,
            }

            return Response(response, status=status.HTTP_201_CREATED)

    def delete(self, request, pie_id):
        pie = get_object_or_404(Pie, id=pie_id)
        # 작성자 체크
        if request.user != pie.writer:
            return Response(
                {
                    'code': status.HTTP_403_FORBIDDEN,
                    'message': 'Permission denied.'
                }
                , status=status.HTTP_403_FORBIDDEN
            )

        pie.delete()
        return Response(
            {
                'code': status.HTTP_200_OK,
                'message': 'PIE DELETE SUCCESSFULLY',
            }
            , status=status.HTTP_200_OK
        )
