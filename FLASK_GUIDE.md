# Guide Flask - FinSight AI

## Migration de Streamlit vers Flask

L'application a été migrée de Streamlit vers Flask pour plus de flexibilité et de contrôle.

## Installation

### 1. Installer les dépendances

```bash
# Activer l'environnement virtuel (si vous en avez un)
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Installer Flask et dépendances
pip install flask flask-session

# Ou installer toutes les dépendances
pip install -r requirements.txt
```

### 2. Configuration

Créez un fichier `.env` à la racine du projet :

**Option 1 : Copier le template**
```bash
# Copiez le fichier template
copy env.template .env  # Windows
# ou
cp env.template .env   # Linux/Mac
```

**Option 2 : Générer une SECRET_KEY automatiquement**
```bash
# Générer une SECRET_KEY aléatoire
py generate_secret_key.py
# ou
python generate_secret_key.py
```

Puis créez votre fichier `.env` avec le contenu suivant :

```env
# Flask Secret Key (OBLIGATOIRE)
# Utilisez la clé générée par generate_secret_key.py
SECRET_KEY=votre_clé_secrète_générée_ici

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
```

**⚠️ IMPORTANT :** 
- La `SECRET_KEY` est **OBLIGATOIRE** pour que Flask fonctionne correctement (sessions, sécurité)
- Ne partagez JAMAIS votre fichier `.env` (il est dans .gitignore)
- En production, utilisez une clé secrète forte générée aléatoirement

## Démarrage

### Option 1 : Utiliser le script de démarrage

```bash
python run_flask.py
```

### Option 2 : Utiliser Flask directement

```bash
flask run
# ou
python app.py
```

### Option 3 : Mode développement

```bash
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows
flask run
```

L'application sera accessible sur : **http://localhost:5000**

## Structure du Projet

```
.
├── app.py                 # Application Flask principale
├── run_flask.py          # Script de démarrage
├── templates/            # Templates HTML
│   ├── base.html         # Template de base
│   ├── dashboard.html    # Page dashboard
│   ├── assistant.html    # Page assistant
│   └── documents.html    # Page documents
├── static/               # Fichiers statiques
│   ├── css/
│   │   └── main.css      # Styles CSS
│   └── js/
│       └── main.js       # JavaScript
└── src/
    └── web/
        └── routes/       # Routes Flask
            ├── dashboard.py
            ├── api.py
            └── chat.py
```

## Routes Disponibles

### Pages
- `/` - Redirige vers le dashboard
- `/dashboard` - Dashboard principal
- `/assistant` - Assistant financier IA
- `/documents` - Explorateur de documents

### API
- `GET /api/quote/<ticker>` - Obtenir le cours d'une action
- `GET /api/overview/<ticker>` - Obtenir les informations de l'entreprise
- `GET /api/timeseries/<ticker>` - Obtenir les données de série temporelle
- `GET /api/chart/price/<ticker>` - Données pour graphique de prix
- `GET /api/chart/rsi/<ticker>` - Données pour graphique RSI
- `POST /api/set-ticker` - Définir le ticker dans la session
- `GET/POST /api/config` - Configuration API keys
- `POST /api/chat/message` - Envoyer un message à l'assistant

## Différences avec Streamlit

1. **Architecture** : Flask utilise une architecture MVC (Model-View-Controller)
2. **Templates** : Utilisation de Jinja2 pour les templates HTML
3. **API REST** : Routes API séparées pour les données
4. **Sessions** : Utilisation de Flask-Session pour gérer les sessions
5. **Frontend** : JavaScript vanilla pour l'interactivité

## Avantages de Flask

- ✅ Plus de contrôle sur le HTML/CSS/JS
- ✅ Meilleure performance
- ✅ API REST séparée
- ✅ Plus facile à déployer
- ✅ Meilleure séparation des préoccupations

## Déploiement

### Production

Pour la production, utilisez un serveur WSGI comme Gunicorn :

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker

Un Dockerfile est disponible pour le déploiement avec Docker.

## Support

Pour toute question ou problème, consultez la documentation technique ou créez une issue.

