from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegistrationView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]