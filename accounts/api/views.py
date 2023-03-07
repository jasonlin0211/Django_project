from accounts.api.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.contrib.auth import(
    authenticate as django_authenticate,
    login as django_login,
    logout as django_logout
)
from accounts.api.serializers import SignupSerializer, LoginSerializer

# api/user/1 -> visit user 1
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]