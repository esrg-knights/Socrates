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
        url(r'^cancel/$', CancelView.as_view(), name="cancel"),
        url(r'^comment/$', CommentView.as_view(), name="comment"),
        url(r'^recipes/$', RecipeView.as_view(), name="recipes"),
        url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', IndexView.as_view(), name="index_specific"),
)
