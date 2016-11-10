from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from api.views import DinnerViewSet, UserViewSet, AchievementViewSet, AchievementGetViewSet

router = routers.DefaultRouter()
router.register(r'dinner', DinnerViewSet)
router.register(r'user', UserViewSet)
router.register(r'achievements/list', AchievementViewSet)
router.register(r'achievements/get', AchievementGetViewSet)

urlpatterns = (
    url(r'^', include(router.urls)),
    url(r'^auth/token/', obtain_jwt_token),
    url(r'^auth/user/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^account/', include('djoser.urls')),
)
