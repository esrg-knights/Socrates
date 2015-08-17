from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'logout/', LogoutView.as_view(), name="logout"),
    url(r'login/', LoginView.as_view(), name="login"),
)
