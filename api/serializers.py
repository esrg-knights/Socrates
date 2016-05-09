from rest_framework import serializers

from dining.models import DiningList, DiningParticipation


class DinnerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiningList


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiningParticipation

class InfoSerializer(serializers.Serializer):
    count = serializers.IntegerField()