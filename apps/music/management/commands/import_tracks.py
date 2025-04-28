import csv
import os
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.music.models import Country, MusicTrack
from tqdm import tqdm  # Import de tqdm pour la barre de progression

class Command(BaseCommand):
    help = "Importe les données musicales depuis le fichier TopSongsSpotify.csv situé dans le dossier data."

    def handle(self, *args, **kwargs):
        # Construction du chemin relatif vers le fichier CSV
        csv_path = os.path.join(settings.BASE_DIR, 'data', 'TopSongsSpotify.csv')
        self.stdout.write(f"Importation depuis : {csv_path}")

        try:
            with open(csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                # Convertir le reader en liste pour connaître le nombre total de lignes
                rows = list(reader)
                # Parcourir chaque ligne avec une barre de progression
                for row in tqdm(rows, desc="Importation", unit="ligne"):
                    # Gestion du champ 'country'
                    country_code = row.get('country')
                    if not country_code or country_code.strip() == "":
                        country_code = "GlobalTop50"
                    country, created = Country.objects.get_or_create(name=country_code.strip())

                    # Conversion de 'snapshot_date' (format attendu: YYYY-MM-DD)
                    try:
                        snapshot_date = datetime.strptime(row.get('snapshot_date', '').strip(), '%Y-%m-%d').date()
                    except Exception:
                        snapshot_date = None

                    # Conversion de 'album_release_date' (optionnelle)
                    album_release_date_str = row.get('album_release_date', '').strip()
                    if album_release_date_str:
                        try:
                            album_release_date = datetime.strptime(album_release_date_str, '%Y-%m-%d').date()
                        except Exception:
                            album_release_date = None
                    else:
                        album_release_date = None

                    # Création de la MusicTrack en convertissant chaque champ
                    MusicTrack.objects.create(
                        spotify_id=row.get('spotify_id', '').strip(),
                        name=row.get('name', '').strip(),
                        artists=row.get('artists', '').strip() if row.get('artists') else None,
                        daily_rank=int(row.get('daily_rank')) if row.get('daily_rank') else None,
                        daily_movement=int(row.get('daily_movement')) if row.get('daily_movement') else None,
                        weekly_movement=int(row.get('weekly_movement')) if row.get('weekly_movement') else None,
                        country=country,
                        snapshot_date=snapshot_date,
                        popularity=int(row.get('popularity')) if row.get('popularity') else None,
                        is_explicit=True if row.get('is_explicit', '').lower() in ('true', '1') else False,
                        duration_ms=int(row.get('duration_ms')) if row.get('duration_ms') else None,
                        album_name=row.get('album_name', '').strip() if row.get('album_name') else None,
                        album_release_date=album_release_date,
                        danceability=float(row.get('danceability')) if row.get('danceability') else None,
                        energy=float(row.get('energy')) if row.get('energy') else None,
                        key=int(row.get('key')) if row.get('key') else None,
                        loudness=float(row.get('loudness')) if row.get('loudness') else None,
                        mode=int(row.get('mode')) if row.get('mode') else None,
                        speechiness=float(row.get('speechiness')) if row.get('speechiness') else None,
                        acousticness=float(row.get('acousticness')) if row.get('acousticness') else None,
                        instrumentalness=float(row.get('instrumentalness')) if row.get('instrumentalness') else None,
                        liveness=float(row.get('liveness')) if row.get('liveness') else None,
                        valence=float(row.get('valence')) if row.get('valence') else None,
                        tempo=float(row.get('tempo')) if row.get('tempo') else None,
                        time_signature=int(row.get('time_signature')) if row.get('time_signature') else None,
                    )
            self.stdout.write(self.style.SUCCESS('Import terminé avec succès.'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Le fichier {csv_path} n'a pas été trouvé."))