# recogogo

Projet d'apprentissage IA / data : un système de recommandation musicale qui, à partir d'une liste de sons en entrée, propose des titres similaires.

## Installation

```bash
python3 -m venv .venv            # crée l'environnement virtuel du projet
source .venv/bin/activate        # l'active (à refaire dans chaque nouveau terminal)
pip install -e ".[dev]"          # installe le projet et ses dépendances
python app/app.py                # lance l'application
```

`-e` (mode éditable) installe un lien vers `src/` au lieu d'une copie. Tes modifications du code sont donc prises en compte sans réinstaller. `[dev]` ajoute les outils de développement (pytest).

## Arborescence

```
recogogo/
├── pyproject.toml      # Dépendances et configuration du projet
├── README.md           # Ce fichier
├── .env                # Secrets (clés d'API) — jamais commité
├── .env.example        # Modèle du .env, sans les valeurs — commité
├── configs/            # Paramètres des expériences (YAML)
├── data/               # Données — ignoré par git
├── artifacts/          # Modèles entraînés, index — ignoré par git
├── src/
│   └── recogogo/       # Le package Python du projet
│       ├── ingestion/  # Collecte des données (API, dumps)
│       └── models/     # Algorithmes de recommandation
├── app/                # Interface utilisateur (Streamlit)
└── test/               # Tests automatisés
```

### Racine

| Fichier | Ce qu'il contient |
|---|---|
| `pyproject.toml` | Nom du projet, version de Python, dépendances (pandas, gensim, implicit…), configuration des outils (pytest, ruff). |
| `.env` | Les secrets, par ex. `LASTFM_API_KEY=abc123`. **Ne jamais le commiter** (déjà couvert par le `.gitignore`). |
| `.env.example` | Les mêmes clés que `.env` mais avec des valeurs vides, pour savoir quoi renseigner après un clone. |

### `configs/`

Les paramètres qu'on fait varier sans toucher au code.

- **À mettre :** un fichier YAML par expérience ou par modèle, par ex. `word2vec.yaml` (`vector_size`, `window`, `epochs`), le `k` du top-K, les chemins de fichiers, le nombre de playlists à collecter.
- **À ne pas mettre :** les secrets (→ `.env`).

### `data/` *(ignoré par git)*

Toutes les données du projet. Elles sont lourdes et régénérables à partir du code, donc hors de git.

- **À mettre :** les dumps téléchargés (ListenBrainz, Million Playlist Dataset), les réponses d'API en cache (Deezer, Last.fm), les jeux nettoyés et les découpages train/test (Parquet).
- **Règle :** les données brutes ne sont jamais modifiées à la main. On les transforme par du code et on écrit le résultat dans un autre fichier.
- **Évolution possible :** séparer en `raw/` (brut, tel que reçu), `interim/` (en cours de nettoyage) et `processed/` (prêt pour l'entraînement).

### `artifacts/` *(ignoré par git)*

Ce que l'entraînement **produit**.

- **À mettre :** modèles sauvegardés (Word2Vec, matrices ALS), index de recherche de voisins (FAISS), embeddings audio pré-calculés.
- **À ne pas mettre :** le code des modèles (→ `src/recogogo/models/`).

### `src/`

Le code Python réutilisable. Ce qui marche dans un notebook et qui va resservir finit ici.

Le code est rangé dans un package `recogogo` installé en mode éditable (voir *Installation*). On l'importe donc de la même façon partout, que ce soit dans `app/`, dans les tests ou dans les notebooks :

```python
from recogogo.ingestion import deezer_api
```

Les fichiers `__init__.py` indiquent à Python qu'un dossier est un package importable.

#### `src/recogogo/ingestion/`

Aller chercher les données et les écrire dans `data/`.

- **À mettre :** un fichier par source, par ex. `deezer.py`, `lastfm.py`, `listenbrainz.py` : appels HTTP, cache, nouvelles tentatives en cas d'erreur, respect des quotas (Deezer : ~50 requêtes / 5 s).
- **À ne pas mettre :** le nettoyage ou la logique de recommandation. Ce module télécharge et stocke, rien de plus.

#### `src/recogogo/models/`

Les approches de recommandation, un fichier par approche, avec la même interface pour toutes (par ex. `fit(train)` et `recommend(titres, k)`) afin de pouvoir les comparer.

- `popularity.py` — baseline : recommande les titres les plus populaires. C'est le score à battre.
- `word2vec.py` — song2vec : deux titres souvent dans les mêmes playlists sont proches.
- `als.py` — factorisation matricielle (bibliothèque `implicit`).
- `hybrid.py` — combinaison collaboratif + contenu (plus tard).

### `app/`

L'interface utilisateur (Streamlit).

- **À mettre :** uniquement de l'affichage — champ de recherche de titres, liste de recommandations, pochettes et extraits audio (via l'API Deezer).
- **À ne pas mettre :** de logique de modèle. L'interface appelle le code de `src/`, ce qui permet de changer de modèle sans la modifier.

### `test/`

Les tests automatisés (pytest).

- **En priorité :** les métriques d'évaluation (recall@k calculé à la main sur un petit exemple) et le découpage train/test (aucun titre du test ne doit fuiter dans le train). Un bug à cet endroit fausse toutes les conclusions sans que ça se voie.

## Sources

Cette organisation s'inspire de :

- [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/) et ses [Opinions](https://cookiecutter-data-science.drivendata.org/opinions/) — découpage des données, notebooks vs code source, secrets hors de git.
- [Python Packaging User Guide — src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) — code dans `src/`.
- [The Twelve-Factor App — Config](https://12factor.net/config) — configuration séparée du code.
- [Microsoft Recommenders](https://github.com/recommenders-team/recommenders) — organisation d'un projet de recommandation (datasets, models, evaluation).
- [Google — Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml) — commencer par un modèle simple et une infrastructure solide.
