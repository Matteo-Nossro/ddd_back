from django.urls import path
from .views import HappinessStatsView, MentalHealthByCountryView

urlpatterns = [
    path('stats/', HappinessStatsView.as_view(), name='happiness-stats'),
    path('mentalhealth/<str:country>/', MentalHealthByCountryView.as_view(), name='mentalhealth-by-country'),
]