# 🔑 Guide : Obtenir la Clé API Gemini (Google)

Ce guide vous explique **étape par étape** comment obtenir votre clé API Gemini pour FinSight AI.

---

## 🎯 Pourquoi Gemini API ?

Gemini est le modèle de langage de Google, offrant des performances comparables à GPT-4 avec des avantages :
- ✅ **Gratuit** pour un usage modéré
- ✅ **Performances élevées** pour l'analyse de texte
- ✅ **Intégration facile** avec LlamaIndex

---

## ✅ Étapes Détaillées

### Étape 1 : Accéder à Google AI Studio

1. **Ouvrez votre navigateur** et allez sur : https://aistudio.google.com/
2. **Connectez-vous** avec votre compte Google
   - Si vous n'avez pas de compte Google, créez-en un gratuitement

### Étape 2 : Créer une Clé API

1. **Une fois connecté**, vous verrez le tableau de bord Google AI Studio
2. **Cliquez sur "Get API Key"** (Obtenir une clé API) en haut à droite
   - Ou allez directement sur : https://aistudio.google.com/app/apikey
3. **Cliquez sur "Create API Key"** (Créer une clé API)
4. **Sélectionnez un projet Google Cloud** :
   - Si vous avez déjà un projet : sélectionnez-le
   - Si vous n'en avez pas : cliquez sur "Create API key in new project"
5. **⚠️ COPIEZ LA CLÉ IMMÉDIATEMENT** - Elle sera affichée une seule fois !
   - La clé ressemble à : `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
6. **Collez-la dans un fichier texte temporaire** pour ne pas la perdre

### Étape 3 : Comprendre les Modèles Disponibles

**Modèles Gemini disponibles** :
- **gemini-pro** : Modèle de base, excellent pour le texte (recommandé)
- **gemini-pro-vision** : Supporte les images en plus du texte

💡 **Pour FinSight AI**, utilisez **gemini-pro** (suffisant pour l'analyse de documents financiers).

### Étape 4 : Comprendre les Limites (Gratuit)

**Plan Gratuit** :
- ✅ **60 requêtes par minute** (RPM)
- ✅ **1500 requêtes par jour** (RPD)
- ✅ **Pas de carte de crédit requise** (pour commencer)
- ✅ **Usage généreux** pour tester et développer

⚠️ **Note** : Si vous dépassez les limites, Google peut vous demander de passer à un plan payant, mais les limites gratuites sont très généreuses.

---

## ⚙️ Configuration dans le Projet

### Étape 1 : Créer le Fichier .env

1. **Ouvrez votre terminal** dans le dossier du projet
2. **Copiez le fichier template** :

   **Windows PowerShell** :
   ```powershell
   Copy-Item env.template .env
   ```

   **Linux/Mac** :
   ```bash
   cp env.template .env
   ```

### Étape 2 : Éditer le Fichier .env

1. **Ouvrez le fichier `.env`** avec un éditeur de texte
2. **Ajoutez votre clé Gemini** :

   ```env
   GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ALPHA_VANTAGE_API_KEY=votre_clé_alpha_vantage_ici
   LLM_MODEL=gemini-pro
   ```

3. **Sauvegardez le fichier**

### Étape 3 : Vérifier le Fichier .env

Votre fichier `.env` devrait ressembler à ceci :

```env
# API Keys
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
ALPHA_VANTAGE_API_KEY=votre_clé_alpha_vantage_ici

# Model Configuration
LLM_MODEL=gemini-pro
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
```

---

## 🧪 Vérification

### Test Rapide de la Clé

1. **Ouvrez un terminal Python** :
   ```bash
   python
   ```

2. **Testez la connexion** :
   ```python
   import os
   from dotenv import load_dotenv
   import google.generativeai as genai

   load_dotenv()
   api_key = os.getenv("GEMINI_API_KEY")
   
   if api_key:
       print("✅ Clé Gemini trouvée")
       # Test simple
       genai.configure(api_key=api_key)
       model = genai.GenerativeModel('gemini-pro')
       response = model.generate_content("Hello, test!")
       print("✅ Connexion Gemini réussie!")
       print(f"Réponse: {response.text}")
   else:
       print("❌ Clé Gemini non trouvée")
   ```

### Test avec l'Application

1. **Lancez l'application** :
   ```bash
   streamlit run src/ui/dashboard.py
   ```

2. **Dans la sidebar**, vérifiez que la clé est chargée
3. **Sélectionnez "gemini-pro"** dans le menu déroulant "LLM Model"
4. **Testez avec un ticker** :
   - Entrez `AAPL` dans le champ "Stock Ticker"
   - Cliquez sur "🚀 Lancer l'Analyse"
   - Si l'application fonctionne, votre clé est correcte ! ✅

---

## 🆘 Problèmes Courants

### Problème : "GEMINI_API_KEY not found"

**Solutions** :
1. Vérifiez que le fichier `.env` existe à la racine du projet
2. Vérifiez que le nom de la variable est exactement `GEMINI_API_KEY`
3. Vérifiez qu'il n'y a pas d'espaces avant/après la clé
4. Redémarrez l'application

### Problème : "Invalid API Key" (Gemini)

**Solutions** :
1. Vérifiez que vous avez copié la clé complète (commence par `AIzaSy`)
2. Vérifiez qu'il n'y a pas d'espaces ou de retours à la ligne
3. Vérifiez que votre clé est active sur https://aistudio.google.com/app/apikey
4. Régénérez une nouvelle clé si nécessaire

### Problème : "Rate limit exceeded"

**Solutions** :
1. Attendez 1 minute (limite de 60 requêtes/minute)
2. Le système gère automatiquement cela
3. Si le problème persiste, vérifiez votre usage sur Google AI Studio

### Problème : "Quota exceeded"

**Solutions** :
1. Vérifiez votre usage quotidien (limite de 1500 requêtes/jour)
2. Attendez jusqu'au lendemain pour que le quota se réinitialise
3. Ou passez à un plan payant si vous avez besoin de plus

---

## 📊 Comparaison Gemini vs OpenAI

| Caractéristique | Gemini (Gratuit) | OpenAI (Payant) |
|----------------|------------------|-----------------|
| **Coût** | Gratuit | ~$5-15 par 1M tokens |
| **Limite RPM** | 60 | Variable selon plan |
| **Limite RPD** | 1500 | Variable selon plan |
| **Performance** | Excellente | Excellente |
| **Carte de crédit** | Non requise | Requise |

💡 **Pour ce projet** : Gemini est parfait car il est gratuit et offre des performances excellentes !

---

## ✅ Checklist Finale

Avant de lancer l'application, vérifiez :

- [ ] Compte Google créé
- [ ] Clé API Gemini obtenue sur https://aistudio.google.com/app/apikey
- [ ] Clé API copiée (commence par `AIzaSy`)
- [ ] Fichier `.env` créé à la racine du projet
- [ ] Clé API ajoutée dans le fichier `.env` comme `GEMINI_API_KEY=...`
- [ ] Fichier `.env` sauvegardé
- [ ] Test de connexion réussi (optionnel)

---

## 🎉 C'est Prêt !

Une fois votre clé Gemini configurée, vous pouvez lancer l'application :

```bash
streamlit run src/ui/dashboard.py
```

**Dans la sidebar** :
- Entrez votre clé Gemini API
- Sélectionnez "gemini-pro" comme modèle
- Commencez à analyser ! 🚀

---

**Besoin d'aide ?** Consultez :
- [QUICKSTART.md](QUICKSTART.md) - Guide de démarrage rapide
- [GUIDE_EXECUTION.md](GUIDE_EXECUTION.md) - Guide d'installation complet
- [README.md](README.md) - Documentation principale






