# ⚡ Quick Start Guide - FinSight AI

Guide rapide pour démarrer en 5 minutes !

## 🚀 Installation Express

### 1. Prérequis
- Python 3.10+
- Clés API (Gemini + Alpha Vantage) - Toutes deux gratuites !

### 2. Installation

```bash
# Cloner le repo
git clone https://github.com/ELMANDOURIHAMZA/FinSight-AI.git
cd "FinSight-AI - Agent Financier Autonome"

# Créer l'environnement virtuel
python -m venv venv

# Activer (Windows)
venv\Scripts\activate

# Activer (Linux/Mac)
source venv/bin/activate

# Installer les dépendances
   pip install -r requirements.txt
```

### 3. Configuration

Créez un fichier `.env` (copiez depuis `env.template`) :
```env
GEMINI_API_KEY=votre_clé_ici
ALPHA_VANTAGE_API_KEY=votre_clé_ici
```

> **🔑 Obtenir les clés** : Consultez [GUIDE_GEMINI_API.md](GUIDE_GEMINI_API.md) pour obtenir votre clé Gemini (gratuit) !

### 4. Lancer

```bash
streamlit run src/ui/dashboard.py
```

Ouvrez `http://localhost:8501` dans votre navigateur !

## 📝 Première Utilisation

1. **Configurez vos clés API** dans la sidebar
2. **Entrez un ticker** (ex: `AAPL`, `MSFT`)
3. **Cliquez sur "Lancer l'Analyse"**
4. **Explorez les onglets** :
   - 📈 Dashboard Marché
   - 💬 Assistant Financier
   - 📄 Explorateur de Documents

## ❓ Questions Fréquentes

**Q: Où obtenir les clés API ?**  
A: **👉 Consultez les guides complets :**
   - **[GUIDE_GEMINI_API.md](GUIDE_GEMINI_API.md)** - Guide pour Gemini (gratuit, recommandé)
   - **[GUIDE_CLES_API.md](GUIDE_CLES_API.md)** - Guide complet pour toutes les clés
   
   Ou directement :
   - Gemini : https://aistudio.google.com/app/apikey (gratuit)
   - Alpha Vantage : https://www.alphavantage.co/support/#api-key (gratuit)

**Q: L'application ne démarre pas ?**  
A: Vérifiez que toutes les dépendances sont installées : `pip install -r requirements.txt`

**Q: Erreur "ModuleNotFoundError" ?**  
A: Assurez-vous que l'environnement virtuel est activé

## 📚 Documentation Complète

Pour plus de détails, consultez :
- **[GUIDE_CLES_API.md](GUIDE_CLES_API.md)** - 🔑 Guide complet pour obtenir les clés API
- [README.md](README.md) - Documentation principale
- [GUIDE_EXECUTION.md](GUIDE_EXECUTION.md) - Guide détaillé pas à pas
- [CAHIER_CHARGES.md](CAHIER_CHARGES.md) - Cahier des charges technique

---

**Besoin d'aide ?** Ouvrez une issue sur GitHub !

