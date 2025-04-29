## Lancement du backend / frontend

### Backend Django

```bash
pip install -r requirements.txt
python manage.py runserver
```

### Frontend vue
Cloner le projet frontend sur :
https://github.com/Matteo-Nossro/ddd_front

Puis :
```bash
npm install
npm run dev
```

## 1. Présentation générale

L’application relie trois domaines :

| Domaine   | Description |
|-----------|-------------|
| **Musique** | Analyse du Top 50 Spotify par pays/date et recommandations de titres similaires. |
| **Bien-être** | Indicateurs _World Happiness Report_ + statistiques de santé mentale (_Global Burden of Disease_). |
| **Analytics** | Vue transversale fusionnant audio-features musicales et indicateurs socio-éco. |

Elle expose un backend Django 5 / DRF et un frontend Vue 3.
Toutes les routes sont paginées (page-number, 20 éléments par défaut).

---

## 2. Architecture DDD

### 2.1 Contextes bornés (_bounded contexts_)

| Contexte (Django app) | Responsabilité | Entités principales |
|-----------------------|----------------|---------------------|
| **accounts** | Authentification JWT, inscription, gestion des utilisateurs (admin). | `User`, `Group` |
| **music** | Charts Spotify, top par date, recherche de similitude. | `Country`, `MusicTrack` |
| **wellbeing** | Données World Happiness + pathologies mentales. | `HappinessRecord`, `MentalHealthRecord` |
| **analytics** | Dataset fusionné `merged_data.csv`. | `MergedDataRecord` |

Chaque contexte accède aux autres **uniquement via leurs endpoints REST**.

### 2.2 Glossaire du langage ubiquitaire
---

### 2.2.1 Entités du domaine

| Terme                   | Description                                                                                            |
|-------------------------|--------------------------------------------------------------------------------------------------------|
| **Country**             | Représente un pays, identifié par son code ISO-2 (`code`). Peut avoir un label humain optionnel (`label`). |
| **Track**               | Représente un morceau de musique, identifié par `spotify_id`. Comprend les métadonnées et les caractéristiques audio. |
| **CountryStatistic**    | Statistiques de bien-être ou de bonheur pour un pays à un instant donné (par ex. `ladder_score`).      |
| **HappinessRecord**     | Classement annuel du bonheur mondial pour un pays (`year`, `rank`, `ladder_score`).                   |
| **MentalHealthRecord**  | Données de santé mentale (prévalence, causes) pour un pays, un groupe d'âge, un sexe et une année donnés. |
| **WellbeingRecord**     | Regroupe les indicateurs de bien-être (p. ex. `HappinessRecord` plus d'autres dimensions si nécessaire). |

---

### 2.2.2 Objets de valeur / Attributs

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

## 3. Gestion des rôles et des accès

| Fonctionnalité | Citizen | Scientist | Admin |
|----------------|:-------:|:---------:|:-----:|
| Top des musiques (pays / date) | ✅ | ✅ | ✅ |
| Suggestions de titres similaires | ✅ | ✅ | ✅ |
| Statistiques pays (analytics + wellbeing) | ❌ | ✅ | ✅ |
| CRUD utilisateurs / rôles | ❌ | ❌ | ✅ |

_Authentification : JWT (DRF + Simple JWT).  
Autorisations : permissions DRF (`IsAdminGroup`, etc.) et garde-routes côté Vue._

---

## 4. Endpoints (tous paginés)

| Méthode & chemin | Rôle requis | Description |
|------------------|-------------|-------------|
| POST `/api/accounts/register` | public | Inscription (username, email, password, password2, role). |
| POST `/api/accounts/token` | public | Access + refresh JWT. |
| POST `/api/accounts/token/refresh` | public | Renouvelle l’access-token. |
| GET/PATCH/DELETE `/api/accounts/users/` | admin | CRUD utilisateurs. |
| GET `/api/accounts/users/stats` | admin | Statistiques globales. |
| GET `/api/music/tracks/<country_code>` | tout | Tous les tracks d’un pays. |
| GET `/api/music/tracks/top/<country_code>/<date>` | tout | Top 50 pour le pays/date. |
| GET `/api/music/tracks/similar/…` | tout | Jusqu’à 5 titres similaires. |
| GET `/api/analytics/stats/<country>` | scientist/admin | Indicateurs fusionnés. |
| GET `/api/wellbeing/stats?country=` | scientist/admin | World Happiness (filtre facultatif). |
| GET `/api/wellbeing/mentalhealth/<country>` | scientist/admin | Pathologies mentales. |

---

## 5. Jeux de données

| Fichier | Modèle cible |
|---------|--------------|
| `TopSongsSpotify.csv` | `MusicTrack` |
| `DataHappiness2025.xlsx` | `HappinessRecord` |
| `DataMentalHealth.csv` | `MentalHealthRecord` |
| `merged_data.csv` | `MergedDataRecord` |

Les migrations importent déjà ces fichiers ; la base `db.sqlite3` fournie est **prête à l’emploi**.

---

## 6. Arborescence simplifiée

```text
ddd/
├─ apps/
│  ├─ accounts/
│  ├─ music/
│  ├─ analytics/
│  └─ wellbeing/
├─ data/
└─ requirements.txt
```

## 7. Utilisateurs par défaut

| Rôle | Username | Mot de passe |
|------|----------|--------------|
| **Admin** | `administrateur` | `admin12345` |
| **Citizen** | `citizen` | `citizen12345` |
| **Scientist** | `scientist` | `scientist12345` |
