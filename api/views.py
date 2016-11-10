from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from achievements.models import Achievement
from api.serializers import DinnerListSerializer, UserWithProfile, AchievementSerializer
from dining.models import DiningList


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1


class DinnerViewSet(ModelViewSet):
    queryset = DiningList.objects.all().order_by("-pk")
    serializer_class = DinnerListSerializer
    pagination_class = StandardResultsSetPagination


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserWithProfile


class AchievementViewSet(ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
