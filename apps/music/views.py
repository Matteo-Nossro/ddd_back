import math
from datetime import datetime

from rest_framework import generics, status
from rest_framework.response import Response

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

class SimilarTracksView(generics.GenericAPIView):
    """
    Renvoie jusqu'à 5 pistes les plus similaires :
      - Référence : (base_country, base_date, spotify_id)
      - Cibles   : (target_country, target_date)
    Similarité : distance Euclidienne sur les audio features.
    """
    serializer_class = MusicTrackSerializer

    def get(self, request,
            base_country, base_date, spotify_id,
            target_country, target_date,
            *args, **kwargs):

        # 1) Parser les dates
        try:
            d_base   = datetime.strptime(base_date, '%Y-%m-%d').date()
            d_target = datetime.strptime(target_date, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"detail": "Format de date invalide, attendu YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2) Charger la piste de référence
        try:
            base = MusicTrack.objects.get(
                country__name__iexact=base_country,    # ← ici
                snapshot_date=d_base,
                spotify_id=spotify_id
            )
        except MusicTrack.DoesNotExist:
            return Response(
                {"detail": "Piste de référence introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 3) Charger les candidates sur target_country/target_date
        candidates = MusicTrack.objects.filter(
            country__name__iexact=target_country,    # ← et ici
            snapshot_date=d_target
        ).exclude(pk=base.pk)

        # 4) Liste des audio features
        feature_fields = [
            'danceability', 'energy', 'key', 'loudness', 'mode',
            'speechiness', 'acousticness', 'instrumentalness',
            'liveness', 'valence', 'tempo'
        ]

        # Valeurs de la piste de référence (0.0 si None)
        base_feats = { f: getattr(base, f) or 0.0 for f in feature_fields }

        # 5) Calcul de la distance pour chaque candidate
        scored = []
        for track in candidates:
            dist2 = sum(
                ((getattr(track, f) or 0.0) - base_feats[f])**2
                for f in feature_fields
            )
            scored.append((math.sqrt(dist2), track))

        # 6) Tri et sélection des 5 plus proches
        scored.sort(key=lambda x: x[0])
        top5 = [t for _, t in scored[:5]]

        # 7) Sérialisation & réponse
        serializer = self.get_serializer(top5, many=True)
        return Response(serializer.data)