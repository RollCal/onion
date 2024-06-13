from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from onions.models import Onion
from .models import Vote

class VoteView(APIView):

    def get_permissions(self):

        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        else:
            pass

        return super().get_permissions()

    def post(self, request):

        request_data = request.data

        target_onion = get_object_or_404(Onion, pk=request_data['onion_id'])

        vote, created = Vote.objects.get_or_create(
            user=request.user,
            onion=target_onion,
        )

        if created or vote.type != request_data.get('type'):
            vote.type = request_data.get('type')
            vote.save()
            response_status = status.HTTP_200_OK
        else:
            vote.delete()
            response_status = status.HTTP_204_NO_CONTENT

        return Response(status=response_status)
