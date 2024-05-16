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
    def get(self, pie_id):
        pie = get_object_or_404(Pie, id=pie_id)
        # 참조 모델 가져오기
        content_type = ContentType.objects.get_for_model(pie)
        # 참조한 모델의 pies 가져오기
        pies = Pie.objects.filter(content_type=content_type, object_id=pie_id)
        serializer = PieSerializer(pies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



