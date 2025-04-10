from datetime import datetime

from rest_framework import generics
from .models import MusicTrack
from .pagination import TopTracksPagination
from .serializers import MusicTrackSerializer

class MusicTrackByCountryListView(generics.ListAPIView):
    """
    Renvoie la liste des pistes musicales pour un pays donné.
    Le pays est identifié par son code (stocké dans le champ 'name' de Country).
    """
    serializer_class = MusicTrackSerializer

    def get_queryset(self):
        # On récupère le paramètre 'country_code' depuis l'URL
        country_code = self.kwargs.get('country_code')
        # On filtre en ignorant la casse (pour plus de flexibilité)
        return MusicTrack.objects.filter(country__name__iexact=country_code)


class TopTracksByCountryAndDateView(generics.ListAPIView):
    """
    Endpoint pour renvoyer le top des pistes d'un pays pour une date donnée.
    Les pistes sont filtrées par le code de pays (insensible à la casse) et par snapshot_date.
    Elles sont triées par daily_rank (les meilleures classes en premier).
    """
    serializer_class = MusicTrackSerializer
    pagination_class = TopTracksPagination

    def get_queryset(self):
        # Récupération des paramètres depuis l'URL
        country_code = self.kwargs.get('country_code')
        date_str = self.kwargs.get('snapshot_date')

        # Filtrage par code de pays (insensible à la casse)
        queryset = MusicTrack.objects.filter(country__name__iexact=country_code)

        # Filtrage par date (snapshot_date)
        try:
            snapshot_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            queryset = queryset.filter(snapshot_date=snapshot_date)
        except ValueError:
            # Si le format de date n'est pas correct, on retourne un QuerySet vide
            queryset = MusicTrack.objects.none()

        # Tri par daily_rank (les meilleurs en premier, i.e. avec le rang le plus faible)
        queryset = queryset.order_by('daily_rank')
        return queryset