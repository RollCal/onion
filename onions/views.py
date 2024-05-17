from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.db.models import F

from pies.models import Pie
from pies.serializers import PieDetailSerializer
from .models import Onion
from .serializers import OnionSerializer, OnionVersusSerializer

class OpinionView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            pass
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def get(self, request, onion_id):
        onion = get_object_or_404(Onion, id=onion_id)
        onion_serializer = OnionSerializer(onion)

        onion.num_of_views = F('num_of_views') + 1
        onion.save()
        onion.refresh_from_db()

        content_type = ContentType.objects.get_for_model(onion)
        pies = Pie.objects.filter(content_type=content_type, object_id=onion_id)
        pie_serializer = PieDetailSerializer(pies, many=True)

        response_data = {
            'onion': onion_serializer.data,
            'pies': pie_serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

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
