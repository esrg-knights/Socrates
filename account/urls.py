from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'logout/', LogoutView.as_view(), name="logout"),
    url(r'login/', LoginView.as_view(), name="login"),
    url(r'register/', RegisterView.as_view(), name="register"),
    url(r'settings/', DetailsView.as_view(), name="settings"),
    url(r'^password/(?P<token>[0-z-]+)/', PasswordChangeView.as_view(), name="change_password_complete"),
    url(r'^password/', PasswordChangeView.as_view(), name="change_password"),
    url(r'activate/(?P<user_hash>[0-z-]+)/', ActivationView.as_view(), name="activate"),
    url(r'^groups/', GroupView.as_view(), name="groups"),
    url(r'^members/', MemberView.as_view(), name="members"),
    url(r'^', IndexView.as_view(), name="index"),
]
