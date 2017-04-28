import django_filters
from requests import Response
from rest_framework import filters, status
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


class DiningListViewset(ModelViewSet):
    serializer_class = DiningListSerializer
    queryset = DiningList.objects.order_by('-relevant_date')[:10]
    filter_fields = ('id', 'owner', 'relevant_date')


class DiningStatsViewset(ModelViewSet):
    serializer_class = DiningStatsSerializer
    queryset = DiningStats.objects.all()
    filter_fields = ('id', 'user')


class DiningParticipationViewset(ModelViewSet):
    serializer_class = DiningParticipationSerializer
    queryset = DiningParticipation.objects.all()
    filter_fields = ('id', 'dining_list', 'work_cook', 'work_groceries', 'work_dishes', 'paid')

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


class UserViewset(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_fields = ('id', 'username', 'email')
