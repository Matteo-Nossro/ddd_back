from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer

class RegistrationView(generics.CreateAPIView):
    """
    Endpoint pour créer un nouveau compte utilisateur.
    On attend en POST : username, email, password, password2 et role.
    """
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer  # Ajustez le chemin d'importation selon votre structure

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer