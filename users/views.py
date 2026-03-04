from django.shortcuts import render
from rest_framework import permissions
from .models import CustomUser
from rest_framework.generics import CreateAPIView
from .serializers import SignUpSerializer


class SignUpView(CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = SignUpSerializer
    queryset = CustomUser
