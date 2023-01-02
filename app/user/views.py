from django.shortcuts import render
from rest_framework import generics
from user.serializer import UserSerializer

# Create your views here.


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
