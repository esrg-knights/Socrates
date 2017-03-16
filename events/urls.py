from django.conf.urls import url, patterns

from events.views import IndexView

urlpatterns = patterns(
    '',
    url(r'^', IndexView.as_view(), name="index"),
)