from django.urls import path
from .views import MusicTrackByCountryListView, TopTracksByCountryAndDateView

urlpatterns = [
    # Endpoint pour obtenir les pistes d'un pays (le paramètre country_code)
    path('tracks/<str:country_code>/', MusicTrackByCountryListView.as_view(), name='music-track-by-country'),
    path('tracks/top/<str:country_code>/<str:snapshot_date>/',
         TopTracksByCountryAndDateView.as_view(),
         name='top-tracks-by-country-date'),
    path(
        'tracks/similar/<str:country_code>/<str:snapshot_date>/<str:spotify_id>/',
        SimilarTracksView.as_view(),
        name='similar-tracks'
    ),
]