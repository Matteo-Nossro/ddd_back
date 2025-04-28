from rest_framework import generics
from .models import MergedDataRecord
from .serializers import MergedDataRecordSerializer

class StatsByCountryView(generics.ListAPIView):
    """
    Endpoint qui renvoie les statistiques (données importées depuis merged_data.csv)
    pour un pays donné.
    
    Le pays est identifié par son code ISO (stocké dans le champ 'country').
    """
    serializer_class = MergedDataRecordSerializer

    def get_queryset(self):
        country_code = self.kwargs.get('country')
        # Filtrer de manière insensible à la casse
        queryset = MergedDataRecord.objects.filter(country__iexact=country_code)
        return queryset.order_by('ladder_score')