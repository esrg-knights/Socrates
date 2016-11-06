from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from api.views import DinnerListView, ParticipationView, InfoView

urlpatterns = (
    url(r'^auth/$', obtain_jwt_token),
    url(r'^latest/participation/$', ParticipationView.as_view()),
    url(r'^latest/info/$', InfoView.as_view()),
    url(r'^latest/$', DinnerListView.as_view()),
)
