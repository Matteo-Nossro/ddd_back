from rest_framework import generics, viewsets, permissions, status
from django.contrib.auth.models import User, Group
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from .serializers import (
    RegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UserManagementSerializer,
    UserUpdateSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView

# Définition d'une permission personnalisée pour le groupe 'admin'
class IsAdminGroup(BasePermission):
    """
    Permission pour vérifier si l'utilisateur appartient au groupe 'admin'
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='admin').exists()

class RegistrationView(generics.CreateAPIView):
    """
    Endpoint pour créer un nouveau compte utilisateur.
    On attend en POST : username, email, password, password2 et role.
    """
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserManagementViewSet(viewsets.ModelViewSet):
    """
    Viewset pour gérer les utilisateurs (admin seulement)
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserManagementSerializer
    permission_classes = [IsAdminGroup]  # Utilisez la permission personnalisée ici

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserManagementSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Retourne des statistiques sur les utilisateurs
        """
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        inactive_users = User.objects.filter(is_active=False).count()

        # Statistiques par rôle
        role_stats = Group.objects.annotate(user_count=Count('user')).values('name', 'user_count')

        # Utilisateurs sans rôle
        users_with_groups = User.objects.filter(groups__isnull=False).distinct().count()
        no_role_count = total_users - users_with_groups

        # Ajouter les utilisateurs sans rôle aux statistiques
        role_stats_list = list(role_stats)
        role_stats_list.append({'name': 'no_role', 'user_count': no_role_count})

        return Response({
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': inactive_users,
            'role_distribution': role_stats_list
        })