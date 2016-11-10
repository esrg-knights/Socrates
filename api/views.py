from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from achievements.models import Achievement, AchievementGet
from api.serializers import DinnerListSerializer, UserWithProfile, AchievementSerializer, SimpleAchievementGetSerializer
from dining.models import DiningList


class SinglePagePagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1


class StandardPaginationation(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class DinnerViewSet(ModelViewSet):
    queryset = DiningList.objects.all().order_by("-pk")
    serializer_class = DinnerListSerializer
    pagination_class = SinglePagePagination


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserWithProfile
    pagination_class = StandardPaginationation


class AchievementViewSet(ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    pagination_class = StandardPaginationation


class AchievementGetViewSet(ModelViewSet):
    queryset = AchievementGet.objects.all().order_by('-score', '-date_achieved')
    serializer_class = SimpleAchievementGetSerializer
    pagination_class = StandardPaginationation
