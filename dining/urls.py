from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^claim/$', ClaimView.as_view(), name="claim"),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', IndexView.as_view(), name="index_specific"),
)
