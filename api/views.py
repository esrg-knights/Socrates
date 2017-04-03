from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import views
from rest_framework import permissions

from achievements.models import Achievement, AchievementGet
from api.serializers import DinnerListSerializer, UserWithProfile, AchievementSerializer, \
    SimpleAchievementGetSerializer, \
    DinnerParticipationSerializer
from dining.models import DiningList, DiningParticipation


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


class DiningParticipationViewset(ModelViewSet):
    serializer_class = DinnerParticipationSerializer
    queryset = DiningParticipation.objects.all()

    def partial_update(self, request, *args, **kwargs):
        if self.is_dinner_owner(request):
            return super(DiningParticipationViewset, self).partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        if self.is_dinner_owner(request):
            return super(DiningParticipationViewset, self).update(request, *args, **kwargs)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        if self.is_dinner_owner(request) or self.is_instance_owner(request):
            return super(DiningParticipationViewset, self).destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def is_dinner_owner(self, request):
        instance = self.get_object()
        return request.user == instance.dining_list.owner

    def is_instance_owner(self, request):
        instance = self.get_object()
        return request.user == instance.user
