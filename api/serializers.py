from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from achievements.models import Achievement, AchievementGet, Game


class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class AchievementGetSerializer(ModelSerializer):
    class Meta:
        model = AchievementGet
        fields = '__all__'


class AchievementSerializer(ModelSerializer):
    related_game = GameSerializer(many=False, read_only=True)

    class Meta:
        model = Achievement
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
