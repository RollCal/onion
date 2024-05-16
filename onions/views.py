from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import OnionSerializer, OnionVersusSerializer

class OpinionView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            pass
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def get(self, request, onion_id):
        pass

    def post(self, request):
        request_data = request.data

        instances = []

        for key in request_data:
            form_data = {
                'title': request_data[key],
                'writer': request.user.pk,
            }

            serializer = OnionSerializer(data=form_data)
            if serializer.is_valid(raise_exception=True):
                instances.append(serializer.save())

        serializer = OnionVersusSerializer(data={
            'purple_onion': instances[0].pk,
            'orange_onion': instances[1].pk,
        })

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

    def put(self, request, onion_id):
        pass

    def delete(self, request, onion_id):
        pass
