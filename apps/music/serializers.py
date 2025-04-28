from rest_framework import serializers
from .models import MusicTrack

class MusicTrackSerializer(serializers.ModelSerializer):
    # Affiche le nom du pays en utilisant la relation (optionnel)
    country = serializers.CharField(source='country.name')

    class Meta:
        model = MusicTrack
        fields = '__all__'