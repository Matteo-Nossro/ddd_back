import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.analyse.models import MergedDataRecord
import pycountry

def get_country_iso(country_name):
    """
    Convertit un nom de pays en code ISO (alpha-2) en utilisant pycountry.
    Retourne None si la conversion échoue.
    """
    try:
        results = pycountry.countries.search_fuzzy(country_name)
        if results:
            return results[0].alpha_2  # Par exemple "France" -> "FR"
    except Exception:
        return None

class Command(BaseCommand):
    help = "Importe les données depuis merged_data.csv dans l'app analyse."

    def handle(self, *args, **kwargs):
        # Construction du chemin relatif vers le fichier CSV
        csv_path = os.path.join(settings.BASE_DIR, 'data', 'merged_data.csv')
        self.stdout.write(f"Importation depuis : {csv_path}")

        try:
            with open(csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    # Lecture et conversion du nom de pays en code ISO
                    raw_country = row.get('country', '').strip()
                    if raw_country:
                        iso_code = get_country_iso(raw_country)
                        country = iso_code if iso_code else raw_country
                    else:
                        country = ""

                    # Fonction utilitaire pour convertir en float
                    def to_float(value):
                        try:
                            return float(value)
                        except Exception:
                            return None

                    record = MergedDataRecord.objects.create(
                        country=country,
                        ladder_score=to_float(row.get('Ladder score')),
                        upperwhisker=to_float(row.get('upperwhisker')),
                        lowerwhisker=to_float(row.get('lowerwhisker')),
                        log_gdp_per_capita=to_float(row.get('Explained by: Log GDP per capita')),
                        social_support=to_float(row.get('Explained by: Social support')),
                        healthy_life_expectancy=to_float(row.get('Explained by: Healthy life expectancy')),
                        freedom_to_make_life_choices=to_float(row.get('Explained by: Freedom to make life choices')),
                        perceptions_of_corruption=to_float(row.get('Explained by: Perceptions of corruption')),
                        dystopia_residual=to_float(row.get('Dystopia + residual')),
                        danceability=to_float(row.get('danceability')),
                        energy=to_float(row.get('energy')),
                        loudness=to_float(row.get('loudness')),
                        acousticness=to_float(row.get('acousticness')),
                        instrumentalness=to_float(row.get('instrumentalness')),
                        valence=to_float(row.get('valence')),
                        tempo=to_float(row.get('tempo')),
                        anxiety_disorders=to_float(row.get('Anxiety disorders')),
                        bipolar_disorder=to_float(row.get('Bipolar disorder')),
                        depressive_disorders=to_float(row.get('Depressive disorders')),
                        mental_disorders=to_float(row.get('Mental disorders')),
                        other_mental_disorders=to_float(row.get('Other mental disorders')),
                        schizophrenia=to_float(row.get('Schizophrenia')),
                    )
                    count += 1
                self.stdout.write(self.style.SUCCESS(f"Import terminé avec succès. {count} enregistrements créés."))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Le fichier {csv_path} n'a pas été trouvé."))