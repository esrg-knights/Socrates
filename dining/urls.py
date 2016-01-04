from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^claim/$', ClaimView.as_view(), name="claim"),
    url(r'^stats/$', StatView.as_view(), name="stats"),
    url(r'^remove/$', RemoveView.as_view(), name="remove"),
    url(r'^extra/$', AddThirdView.as_view(), name="extra"),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', IndexView.as_view(), name="index_specific"),
)
