from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet

from api.serializers import UserSerializer


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = ()
    filter_fields = ('id',)
