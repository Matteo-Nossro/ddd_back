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

class MentalHealthRecord(models.Model):
    measure_id = models.IntegerField(null=True, blank=True)
    measure_name = models.CharField(max_length=255, null=True, blank=True)
    location_id = models.IntegerField(null=True, blank=True)
    location_name = models.CharField(max_length=255, null=True, blank=True)
    sex_id = models.IntegerField(null=True, blank=True)
    sex_name = models.CharField(max_length=255, null=True, blank=True)
    age_id = models.IntegerField(null=True, blank=True)
    age_name = models.CharField(max_length=255, null=True, blank=True)
    cause_id = models.IntegerField(null=True, blank=True)
    cause_name = models.CharField(max_length=255, null=True, blank=True)
    metric_id = models.IntegerField(null=True, blank=True)
    metric_name = models.CharField(max_length=255, null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    val = models.FloatField(null=True, blank=True)
    upper = models.FloatField(null=True, blank=True)
    lower = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.location_name} - {self.year} ({self.cause_name})"