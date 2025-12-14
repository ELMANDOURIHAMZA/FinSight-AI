# FinSight AI - Application Flask

## 🚀 Démarrage Rapide

### Installation

1. **Installer Flask et dépendances** :
```bash
pip install flask flask-session
# ou
pip install -r requirements.txt
```

2. **Configurer les variables d'environnement** :
Créez un fichier `.env` :
```env
GEMINI_API_KEY=your_key_here
ALPHA_VANTAGE_API_KEY=your_key_here
SECRET_KEY=your-secret-key
```

3. **Lancer l'application** :
```bash
python run_flask.py
```

L'application sera accessible sur **http://localhost:5000**

## 📁 Structure

- `app.py` - Application Flask principale
- `run_flask.py` - Script de démarrage
- `templates/` - Templates HTML (Jinja2)
- `static/` - CSS, JavaScript, images
- `src/web/routes/` - Routes Flask (blueprints)

## 🎨 Design

L'application utilise le même design Analytics Dashboard que la version Streamlit, avec :
- Sidebar de navigation
- Cartes de métriques
- Graphiques interactifs (Plotly.js)
- Design moderne et professionnel

## 📚 Documentation

Consultez `FLASK_GUIDE.md` pour plus de détails.

