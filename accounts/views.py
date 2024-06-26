import random
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from onions.tasks import send_alert
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User

class AccountListAPIView(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            pass
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def post(self, request):

        request_data = request.data

        confirm = request_data.get('confirm')

        if confirm is None:
            return Response(data={
                'error': 'confirm is None'
            }, status=status.HTTP_400_BAD_REQUEST)

        if confirm != cache.get(request_data.get("email")):
            return Response(data={
                'error': 'confirm number does not match'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            cache.delete(request_data.get("email"))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def email_confirm(request):
    email = request.data.get('email')

    if User.objects.filter(email=email).exists():
        return Response(data={
            "error": "해당 이메일은 이미 존재합니다"
        }, status=status.HTTP_400_BAD_REQUEST)

    if email is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if cache.get(email):
        return Response(data={
            'error': '이메일 인증 메일이 이미 전송되었습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)
    else:
        confirm_number = ''.join(random.choices('0123456789', k=5))
        cache.set(email, confirm_number, 60 * 3)

        send_alert(
            type="confirm",
            to_email=email,
            data={
                'confirm_number': confirm_number,
            }
        )
        return Response(status=status.HTTP_200_OK)
