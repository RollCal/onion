from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from onions.models import Onion
from pies.models import Pie
from .models import Vote
from django.contrib.contenttypes.models import ContentType

class VoteView(APIView):

    def get_permissions(self):

        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        else:
            pass

        return super().get_permissions()

    def post(self, request):
        request_data = request.data
        content_type = request_data.get('content_type')
        obj_id = request_data['id']

        if content_type == 'onion':
            model_cls = Onion
        elif content_type == 'pie':
            model_cls = Pie
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        content_type = ContentType.objects.get_for_model(model_cls)
        obj = get_object_or_404(model_cls, id=obj_id)

        vote, created = Vote.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj.id,
        )

        if created or vote.type != request_data.get('type'):
            vote.type = request_data.get('type')
            vote.save()
            response_status = status.HTTP_200_OK
        else:
            vote.delete()
            response_status = status.HTTP_204_NO_CONTENT

        return Response(status=response_status)
