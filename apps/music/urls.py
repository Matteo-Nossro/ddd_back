from django.urls import path
from .views import MusicTrackByCountryListView, TopTracksByCountryAndDateView, SimilarTracksView

urlpatterns = [
    # Endpoint pour obtenir les pistes d'un pays (le paramètre country_code)
    path('tracks/<str:country_code>/', MusicTrackByCountryListView.as_view(), name='music-track-by-country'),
    path('tracks/top/<str:country_code>/<str:snapshot_date>/',
         TopTracksByCountryAndDateView.as_view(),
         name='top-tracks-by-country-date'),
    path(
        'tracks/similar/'
        '<str:base_country>/<str:base_date>/<str:spotify_id>/'
        '<str:target_country>/<str:target_date>/',
        SimilarTracksView.as_view(),
        name='similar-tracks'
    ),
]