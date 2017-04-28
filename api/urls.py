from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from api.views import *

router = routers.DefaultRouter()
router.register(r'user', UserViewset)
router.register(r'achievement', AchievementViewset)
router.register(r'achievementget', AchievementGetViewset)

urlpatterns = (
    url(r'^models/', include(router.urls)),
    url(r'^auth/token/', obtain_jwt_token),
    url(r'^auth/refresh', refresh_jwt_token),
    url(r'^auth/user/', include('rest_framework.urls',
                                namespace='rest_framework')),
    url(r'^account/', include('djoser.urls')),
)
