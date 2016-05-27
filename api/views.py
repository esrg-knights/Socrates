from django.http import HttpResponse

# Create your views here.
from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import DinnerListSerializer, InfoSerializer
from dining.models import DiningList


class DinnerListView(APIView):
    def get(self, request, format=None):
        return Response(DinnerListSerializer(DiningList.get_latest()).data)


class ParticipationView(APIView):
    def get(self, request, format=None):
        parts = serializers.serialize('json', DiningList.get_latest().get_participants())
        return HttpResponse(parts, content_type='json')


class InfoView(APIView):
    def get(self, request, format=None):
        dining_list = DiningList.get_latest()

        data = {
            "count": len(dining_list.get_participants()),
            "participants": dining_list.get_participants()
        }

        return Response(InfoSerializer(data).data)
