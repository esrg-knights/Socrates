import django_filters
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import *


class AchievementGetViewset(ModelViewSet):
    serializer_class = AchievementGetSerializer
    queryset = AchievementGet.objects.all()
    filter_fields = ('id', 'user', 'achievement', 'awarded_by')


class AchievementViewset(ModelViewSet):
    serializer_class = AchievementSerializer
    queryset = Achievement.objects.filter(is_public=True)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ('id', 'category', 'related_game')
    ordering_fields = ('date_created', 'date_last_accessed')


class UserViewset(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_fields = ('id', 'username', 'email')
