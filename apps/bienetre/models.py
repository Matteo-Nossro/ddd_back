from django.db import models

class HappinessRecord(models.Model):
    year = models.PositiveIntegerField()
    rank = models.PositiveIntegerField()
    country_name = models.CharField(max_length=255)
    ladder_score = models.FloatField(null=True, blank=True)
    upperwhisker = models.FloatField(null=True, blank=True)
    lowerwhisker = models.FloatField(null=True, blank=True)
    log_gdp_per_capita = models.FloatField(null=True, blank=True)   # Modification ici
    social_support = models.FloatField(null=True, blank=True)
    healthy_life_expectancy = models.FloatField(null=True, blank=True)
    freedom_to_make_life_choices = models.FloatField(null=True, blank=True)
    generosity = models.FloatField(null=True, blank=True)
    perceptions_of_corruption = models.FloatField(null=True, blank=True)
    dystopia_residual = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.country_name} - {self.year} (Score: {self.ladder_score})"