from django.conf.urls import url

from api.views import DinnerListView, ParticipationView, InfoView

urlpatterns = (
    url(r'^latest/participation/$', ParticipationView.as_view()),
    url(r'^latest/info/$', InfoView.as_view()),
    url(r'^latest/$', DinnerListView.as_view()),
)
