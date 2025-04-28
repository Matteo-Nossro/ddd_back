## Glossaire du langage ubiquitaire

Ce document définit tous les termes du langage ubiquitaire utilisés dans le projet Django, organisés par catégorie.

---

### 1. Entités du domaine

| Terme                   | Description                                                                                            |
|-------------------------|--------------------------------------------------------------------------------------------------------|
| **Country**             | Représente un pays, identifié par son code ISO-2 (`code`). Peut avoir un label humain optionnel (`label`). |
| **Track**               | Représente un morceau de musique, identifié par `spotify_id`. Comprend les métadonnées et les caractéristiques audio. |
| **CountryStatistic**    | Statistiques de bien-être ou de bonheur pour un pays à un instant donné (par ex. `ladder_score`).      |
| **HappinessRecord**     | Classement annuel du bonheur mondial pour un pays (`year`, `rank`, `ladder_score`).                   |
| **MentalHealthRecord**  | Données de santé mentale (prévalence, causes) pour un pays, un groupe d'âge, un sexe et une année donnés. |
| **WellbeingRecord**     | Regroupe les indicateurs de bien-être (p. ex. `HappinessRecord` plus d'autres dimensions si nécessaire). |

---

### 2. Objets de valeur / Attributs

| Terme                             | Type        | Description                                                                          |
|-----------------------------------|-------------|--------------------------------------------------------------------------------------|
| **country_code**                  | CharField   | Code ISO-2 du pays (ex. `FR`, `US`). Utilisé pour filtrer les données.               |
| **snapshot_date**                 | DateField   | Date à laquelle les données (morceaux ou statistiques) ont été capturées.            |
| **ladder_score**                  | FloatField  | Score de bonheur attribué à un pays (échelle 0–10).                                   |
| **upper_whisker**                 | FloatField  | Valeur supérieure de la moustache dans un diagramme en boîte.                        |
| **lower_whisker**                 | FloatField  | Valeur inférieure de la moustache dans un diagramme en boîte.                        |
| **log_gdp_per_capita**            | FloatField  | Logarithme du PIB par habitant, indicateur économique.                               |
| **social_support**                | FloatField  | Niveau de soutien social perçu dans le pays.                                         |
| **healthy_life_expectancy**       | FloatField  | Espérance de vie en bonne santé.                                                     |
| **freedom_to_make_life_choices**  | FloatField  | Degré de liberté perçue pour faire des choix de vie.                                |
| **perceptions_of_corruption**     | FloatField  | Indice de perception de la corruption.                                               |
| **dystopia_residual**             | FloatField  | Résidu du modèle pour une dystopie hypothétique de référence.                        |
| **danceability**                  | FloatField  | Caractéristique audio Spotify (0.0–1.0) indiquant l'aptitude à danser.               |
| **energy**                        | FloatField  | Caractéristique audio Spotify (0.0–1.0) mesurant l'intensité et l'énergie du morceau.|
| **loudness**                      | FloatField  | Volume moyen du morceau en décibels (dB).                                            |
| **acousticness**                  | FloatField  | Probabilité que le morceau soit acoustique.                                          |
| **instrumentalness**              | FloatField  | Probabilité qu'il n'y ait pas de voix dans le morceau.                              |
| **valence**                       | FloatField  | Degré de positivité émotionnelle du morceau (0.0 triste, 1.0 joyeux).               |
| **tempo**                         | FloatField  | Nombre de battements par minute du morceau.                                          |

---

### 3. Services / Endpoints

| Endpoint                                                                                  | Verbe HTTP | Description                                                                                       |
|-------------------------------------------------------------------------------------------|------------|---------------------------------------------------------------------------------------------------|
| `GET /countries/{country_code}/tracks/`                                                   | GET        | Liste de tous les `Track` pour un pays donné.                                                     |
| `GET /countries/{country_code}/tracks/top/{snapshot_date}/`                               | GET        | Top des `Track` ordonné par `daily_rank` pour une date donnée.                                    |
| `GET /countries/{country_code}/tracks/{snapshot_date}/{spotify_id}/similar/`              | GET        | Jusqu'à 5 `Track` les plus similaires à la `Track` de référence (distance Euclidienne sur les caractéristiques audio). |
| `GET /stats/{country_code}/`                                                              | GET        | Liste de tous les `CountryStatistic` pour un pays donné.                                          |
| `GET /happiness/`                                                                         | GET        | Tous les enregistrements `HappinessRecord` (filtrables via `?country={country_code}`).            |
| `GET /mentalhealth/{country_code}/`                                                       | GET        | Tous les enregistrements `MentalHealthRecord` pour un pays donné.                                  |

---

### 4. Termes & concepts métier

- **Snapshot** : Représentation des données à un instant précis (`snapshot_date`).
- **Similarity Score** : Distance Euclidienne entre les vecteurs de caractéristiques audio.
- **Whiskers** : Bornes statistiques utilisées dans les diagrammes en boîte.
- **Ladder Score** : Score de bonheur sur une échelle fixe (0–10) issu du World Happiness Report.  