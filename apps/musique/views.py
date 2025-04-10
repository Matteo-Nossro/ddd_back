from rest_framework import generics
from .models import MusicTrack
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