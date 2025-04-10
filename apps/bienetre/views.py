from rest_framework import generics
from .models import HappinessRecord
from .serializers import HappinessRecordSerializer

class HappinessStatsView(generics.ListAPIView):
    """
    API qui renvoie les enregistrements de bien-être (HappinessRecord) en fonction d'un pays donné.
    Si le paramètre 'country' de la query string vaut 'all' ou n'est pas fourni, renvoie tous les enregistrements.
    """
    serializer_class = HappinessRecordSerializer

    def get_queryset(self):
        # Récupération du paramètre 'country' dans la query string, par ex. ?country=FR
        country = self.request.query_params.get('country', None)
        if not country or country.lower() == 'all':
            queryset = HappinessRecord.objects.all()
        else:
            queryset = HappinessRecord.objects.filter(country_name__iexact=country)
        # Vous pouvez ordonner par année, par exemple
        return queryset.order_by('year')