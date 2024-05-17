from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer
from .serializers import ProfileSerializer

class ProfileView(APIView):
    # 권한 확인
    def get_permissions(self):
        if self.request.method == 'GET':
            pass
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()
    # 유저 프로필 조회
    def get(self, request, user_id):
        user = get_object_or_404(get_user_model(), pk=user_id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        pass
    # 회원 정보(비밀번호) 변경
    def put(self, request, user_id):
        user = get_object_or_404(get_user_model(), pk=user_id)
        # 요청 유저와 수정 프로필 유저 일치 확인
        if request.user != user:
            return Response({"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        # 비밀번호 검증은 UserSerializer안에 구현되어있음 partial은 나중에 수정 요소 추가될까봐 넣어둠
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
class ProfileOnionsListView(APIView):
    pass

# 관리자 권한 조정
class AdjustPermissionView(APIView):
    # 권한 확인
    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
    def put(self, request, user_id):
        pass
