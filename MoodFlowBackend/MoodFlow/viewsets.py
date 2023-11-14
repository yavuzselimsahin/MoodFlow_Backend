from rest_framework import viewsets
from . import models
from . import serializer

class UserViewset(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializer.UserSerializer