from rest_framework import generics
from .models import HappinessRecord, MentalHealthRecord
from .serializers import HappinessRecordSerializer, MentalHealthRecordSerializer


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


class MentalHealthByCountryView(generics.ListAPIView):
    """
    Endpoint qui renvoie les enregistrements de santé mentale (les maladies)
    pour un pays donné.

    Le pays est identifié par son code ISO (stocké dans 'location_name').
    """
    serializer_class = MentalHealthRecordSerializer

    def get_queryset(self):
        # Récupérer le paramètre country depuis l'URL
        country_code = self.kwargs.get('country')
        # Filtrer avec une comparaison insensible à la casse
        queryset = MentalHealthRecord.objects.filter(location_name__iexact=country_code)
        # Optionnel : Vous pouvez ordonner le queryset, par exemple par année ou par cause
        return queryset.order_by('year')