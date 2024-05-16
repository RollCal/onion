from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import PieSerializer
from onions.models import Onion
from .models import Pie


# Create your views here.
class PiesAPIView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            pass
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    # pie 목록 조회
    def get(self, object_type, object_id):
        # 시각화된 pie 의 pies
        if object_type == 'pie':
            obj = get_object_or_404(Pie, id=object_id)
        # onion의 pies
        elif object_type == 'onion':
            obj = get_object_or_404(Onion, id=object_id)
        # 둘다 아닐때 not found
        else:
            return Response(
                {
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': '404 NOT FOUND',
                 },
                status=status.HTTP_404_NOT_FOUND)
        # 참조 모델 가져오기
        content_type = ContentType.objects.get_for_model(obj)
        # 참조한 모델의 pies 가져오기
        pies = Pie.objects.filter(content_type=content_type, object_id=object_id)
        serializer = PieSerializer(pies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



