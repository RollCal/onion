from rest_framework.permissions import IsAuthenticated
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
        # 회원가입 또는 로그인하기
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        # 토큰 발급하기
        token_obtain_pair_view = TokenObtainPairView.as_view()
        token_response = token_obtain_pair_view(request=request._request)

        if token_response.status_code == status.HTTP_200_OK:
            response_data = {
                'user': serializer.data,
                'tokens': token_response.data
            }
            # 클라이언트에게 토큰 저장 요청 추가
            response = Response(response_data, status=status.HTTP_201_CREATED)

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
