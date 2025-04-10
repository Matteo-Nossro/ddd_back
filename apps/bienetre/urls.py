from django.urls import path
from .views import HappinessStatsView

urlpatterns = [
    path('stats/', HappinessStatsView.as_view(), name='happiness-stats'),
]