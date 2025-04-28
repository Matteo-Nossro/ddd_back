from django.db import models

# Create your models here.
class Country(models.Model):
    # Ici, on stocke le code ISO ou le label du pays.
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class MusicTrack(models.Model):
    spotify_id = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    artists = models.CharField(max_length=255, null=True, blank=True)  # optionnelle
    daily_rank = models.IntegerField(null=True, blank=True)
    daily_movement = models.IntegerField(null=True, blank=True)
    weekly_movement = models.IntegerField(null=True, blank=True)
    # La relation Country est obligatoire ; on gérera le cas d'une donnée absente pour country en créant ou utilisant un pays avec le nom "GlobalTop50".
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='tracks')
    snapshot_date = models.DateField()
    popularity = models.IntegerField(null=True, blank=True)
    is_explicit = models.BooleanField(default=False)
    duration_ms = models.IntegerField(null=True, blank=True)
    album_name = models.CharField(max_length=255, null=True, blank=True)  # optionnelle
    album_release_date = models.DateField(null=True, blank=True)  # optionnelle
    danceability = models.FloatField(null=True, blank=True)
    energy = models.FloatField(null=True, blank=True)
    key = models.IntegerField(null=True, blank=True)
    loudness = models.FloatField(null=True, blank=True)
    mode = models.IntegerField(null=True, blank=True)
    speechiness = models.FloatField(null=True, blank=True)
    acousticness = models.FloatField(null=True, blank=True)
    instrumentalness = models.FloatField(null=True, blank=True)
    liveness = models.FloatField(null=True, blank=True)
    valence = models.FloatField(null=True, blank=True)
    tempo = models.FloatField(null=True, blank=True)
    time_signature = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.country.name})"