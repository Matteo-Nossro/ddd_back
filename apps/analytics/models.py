from django.db import models

class MergedDataRecord(models.Model):
    country = models.CharField(max_length=10)  # Code ISO (alpha-2) du pays
    ladder_score = models.FloatField(null=True, blank=True)
    upperwhisker = models.FloatField(null=True, blank=True)
    lowerwhisker = models.FloatField(null=True, blank=True)
    log_gdp_per_capita = models.FloatField(null=True, blank=True)
    social_support = models.FloatField(null=True, blank=True)
    healthy_life_expectancy = models.FloatField(null=True, blank=True)
    freedom_to_make_life_choices = models.FloatField(null=True, blank=True)
    perceptions_of_corruption = models.FloatField(null=True, blank=True)
    dystopia_residual = models.FloatField(null=True, blank=True)
    danceability = models.FloatField(null=True, blank=True)
    energy = models.FloatField(null=True, blank=True)
    loudness = models.FloatField(null=True, blank=True)
    acousticness = models.FloatField(null=True, blank=True)
    instrumentalness = models.FloatField(null=True, blank=True)
    valence = models.FloatField(null=True, blank=True)
    tempo = models.FloatField(null=True, blank=True)
    anxiety_disorders = models.FloatField(null=True, blank=True)
    bipolar_disorder = models.FloatField(null=True, blank=True)
    depressive_disorders = models.FloatField(null=True, blank=True)
    mental_disorders = models.FloatField(null=True, blank=True)
    other_mental_disorders = models.FloatField(null=True, blank=True)
    schizophrenia = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.country} - Ladder: {self.ladder_score}"