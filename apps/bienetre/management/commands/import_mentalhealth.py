import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.bienetre.models import MentalHealthRecord
import pycountry

def get_country_iso(country_name):
    """
    Convertit un nom de pays en code ISO (alpha-2) en utilisant pycountry.
    Retourne None si la conversion échoue.
    """
    try:
        results = pycountry.countries.search_fuzzy(country_name)
        if results:
            return results[0].alpha_2
    except Exception:
        return None

class Command(BaseCommand):
    help = "Importe les données de santé mentale depuis le fichier DataMentalHealth.csv."

    def handle(self, *args, **kwargs):
        # Construction du chemin vers le fichier CSV
        csv_path = os.path.join(settings.BASE_DIR, 'data', 'DataMentalHealth.csv')
        self.stdout.write(f"Importation depuis : {csv_path}")

        try:
            with open(csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    # Conversion des champs numériques ou textuels
                    try:
                        measure_id = int(row.get('measure_id')) if row.get('measure_id') else None
                    except Exception:
                        measure_id = None

                    measure_name = row.get('measure_name', '').strip() or None
                    try:
                        location_id = int(row.get('location_id')) if row.get('location_id') else None
                    except Exception:
                        location_id = None

                    # Récupération du nom du pays et conversion en code ISO
                    raw_location_name = row.get('location_name', '').strip()
                    if raw_location_name:
                        iso_code = get_country_iso(raw_location_name)
                        # Si conversion réussit, on stocke le code ISO, sinon on garde le nom original
                        location_name = iso_code if iso_code else raw_location_name
                    else:
                        location_name = None

                    try:
                        sex_id = int(row.get('sex_id')) if row.get('sex_id') else None
                    except Exception:
                        sex_id = None

                    sex_name = row.get('sex_name', '').strip() or None
                    try:
                        age_id = int(row.get('age_id')) if row.get('age_id') else None
                    except Exception:
                        age_id = None

                    age_name = row.get('age_name', '').strip() or None
                    try:
                        cause_id = int(row.get('cause_id')) if row.get('cause_id') else None
                    except Exception:
                        cause_id = None

                    cause_name = row.get('cause_name', '').strip() or None
                    try:
                        metric_id = int(row.get('metric_id')) if row.get('metric_id') else None
                    except Exception:
                        metric_id = None

                    metric_name = row.get('metric_name', '').strip() or None

                    try:
                        year = int(row.get('year')) if row.get('year') else None
                    except Exception:
                        year = None

                    try:
                        val = float(row.get('val')) if row.get('val') else None
                    except Exception:
                        val = None

                    try:
                        upper = float(row.get('upper')) if row.get('upper') else None
                    except Exception:
                        upper = None

                    try:
                        lower = float(row.get('lower')) if row.get('lower') else None
                    except Exception:
                        lower = None

                    MentalHealthRecord.objects.create(
                        measure_id=measure_id,
                        measure_name=measure_name,
                        location_id=location_id,
                        location_name=location_name,
                        sex_id=sex_id,
                        sex_name=sex_name,
                        age_id=age_id,
                        age_name=age_name,
                        cause_id=cause_id,
                        cause_name=cause_name,
                        metric_id=metric_id,
                        metric_name=metric_name,
                        year=year,
                        val=val,
                        upper=upper,
                        lower=lower,
                    )
                    count += 1
                self.stdout.write(self.style.SUCCESS(f"Import terminé avec succès. {count} enregistrements créés."))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Le fichier {csv_path} n'a pas été trouvé."))