from django.urls import path
from .views import MusicTrackByCountryListView

urlpatterns = [
    # Endpoint pour obtenir les pistes d'un pays (le paramètre country_code)
    path('tracks/<str:country_code>/', MusicTrackByCountryListView.as_view(), name='music-track-by-country'),
]