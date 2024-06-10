import random

from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from onions.tasks import send_alert
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def email_confirm(request):
    email = request.data.get('email')

    if email is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if cache.get(email):
        return Response(data={
            'error': '이메일 인증 메일이 이미 전송되었습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)
    else:
        confirm_number = ''.join(random.choices('0123456789', k=5))
        send_alert(
            type="confirm",
            to_email=email,
            data={
                'confirm_number': confirm_number,
            }
        )
        cache.set(email, confirm_number, 60*3)
        return Response(status=status.HTTP_200_OK)
