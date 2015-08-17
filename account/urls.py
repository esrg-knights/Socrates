from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'logout/', LogoutView.as_view(), name="logout"),
    url(r'login/', LoginView.as_view(), name="login"),
    url(r'register/', RegisterView.as_view(), name="register"),
    url(r'activate/(?P<user_hash>\w+)/', ActivationView.as_view(), name="activate"),
)
