from django.urls import path
from .views import StatsByCountryView

urlpatterns = [
    path('stats/<str:country>/', StatsByCountryView.as_view(), name='stats-by-country'),
]