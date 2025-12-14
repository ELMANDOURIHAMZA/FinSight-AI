# 🔑 Guide Complet : Obtenir les Clés API

Ce guide vous explique **étape par étape** comment obtenir les clés API nécessaires pour FinSight AI.

> **💡 Note** : Le projet utilise maintenant **Gemini (Google)** par défaut au lieu d'OpenAI. Gemini est gratuit et offre d'excellentes performances !

---

## 📋 Table des Matières

1. [Clé API Gemini (Google) - RECOMMANDÉ](#1-clé-api-gemini-google---recommandé)
2. [Clé API Alpha Vantage](#2-clé-api-alpha-vantage)
3. [Clé API OpenAI (Optionnel)](#3-clé-api-openai-optionnel)
4. [Configuration dans le Projet](#4-configuration-dans-le-projet)
5. [Vérification](#5-vérification)

---

## 1. Clé API Gemini (Google) - RECOMMANDÉ

> **👉 Guide détaillé** : Consultez **[GUIDE_GEMINI_API.md](GUIDE_GEMINI_API.md)** pour un guide complet étape par étape.

### 🎯 Pourquoi Gemini API ?

Gemini est le modèle de langage de Google, offrant :
- ✅ **Gratuit** pour un usage modéré
- ✅ **Performances élevées** comparables à GPT-4
- ✅ **60 requêtes/minute** et **1500 requêtes/jour** (gratuit)
- ✅ **Pas de carte de crédit requise**

### ✅ Étapes Rapides

1. **Allez sur** : https://aistudio.google.com/app/apikey
2. **Connectez-vous** avec votre compte Google
3. **Cliquez sur "Create API Key"**
4. **Copiez la clé** (commence par `AIzaSy...`)
5. **Ajoutez-la dans votre fichier `.env`** comme `GEMINI_API_KEY=...`

---

## 2. Clé API Alpha Vantage

### 🎯 Pourquoi OpenAI API ?

OpenAI API est nécessaire pour utiliser les modèles de langage (GPT-4o, GPT-3.5-turbo) qui alimentent l'agent financier et le système RAG.

### ✅ Étapes Détaillées

#### Étape 1 : Créer un Compte OpenAI

1. **Ouvrez votre navigateur** et allez sur : https://platform.openai.com/
2. **Cliquez sur "Sign up"** (S'inscrire) en haut à droite
3. **Remplissez le formulaire** :
   - Email
   - Mot de passe (minimum 8 caractères)
   - Acceptez les conditions d'utilisation
4. **Vérifiez votre email** : OpenAI vous enverra un email de confirmation
5. **Cliquez sur le lien** dans l'email pour confirmer votre compte

#### Étape 2 : Ajouter une Méthode de Paiement (Optionnel mais Recommandé)

⚠️ **Important** : Même si OpenAI offre des crédits gratuits, vous devrez peut-être ajouter une carte de crédit pour certaines fonctionnalités.

1. **Connectez-vous** à https://platform.openai.com/
2. **Cliquez sur votre profil** (icône en haut à droite)
3. **Sélectionnez "Billing"** (Facturation)
4. **Cliquez sur "Add payment method"** (Ajouter un moyen de paiement)
5. **Remplissez les informations** de votre carte bancaire
6. **Confirmez** l'ajout

💡 **Note** : OpenAI offre généralement **$5 de crédits gratuits** pour les nouveaux comptes, ce qui est suffisant pour tester le projet.

#### Étape 3 : Créer une Clé API

1. **Allez sur** : https://platform.openai.com/api-keys
   - Ou : Connectez-vous → Cliquez sur votre profil → "API keys"
2. **Cliquez sur "Create new secret key"** (Créer une nouvelle clé secrète)
3. **Donnez un nom** à votre clé (ex: "FinSight AI - Projet Portfolio")
4. **Cliquez sur "Create secret key"**
5. **⚠️ COPIEZ LA CLÉ IMMÉDIATEMENT** - Elle ne sera affichée qu'une seule fois !
   - La clé ressemble à : `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
6. **Collez-la dans un fichier texte temporaire** pour ne pas la perdre

#### Étape 4 : Comprendre les Coûts

**Modèles disponibles** :
- **GPT-4o** : Plus performant, plus cher (~$5-15 par 1M tokens)
- **GPT-3.5-turbo** : Moins cher, toujours performant (~$0.50-1.50 par 1M tokens)

💡 **Conseil** : Pour tester, utilisez `gpt-3.5-turbo` dans votre fichier `.env` pour économiser.

**Limites** :
- OpenAI peut avoir des limites de taux (rate limits) selon votre plan
- Surveillez votre utilisation sur https://platform.openai.com/usage

---

## 2. Clé API Alpha Vantage

### 🎯 Pourquoi Alpha Vantage API ?

Alpha Vantage fournit les données boursières en temps réel (prix, volumes, indicateurs techniques) nécessaires au dashboard.

### ✅ Étapes Détaillées

#### Étape 1 : Aller sur le Site Alpha Vantage

1. **Ouvrez votre navigateur** et allez sur : https://www.alphavantage.co/support/#api-key
2. **Faites défiler** jusqu'à la section "Get Your Free API Key"

#### Étape 2 : Remplir le Formulaire

Le formulaire demande :
- **Email** : Votre adresse email valide
- **First Name** : Votre prénom
- **Last Name** : Votre nom
- **Organization** : Nom de votre organisation (peut être "Personal" ou votre nom)
- **Usage** : Sélectionnez "Individual/Personal Use"

#### Étape 3 : Soumettre et Recevoir la Clé

1. **Cliquez sur "GET FREE API KEY"**
2. **Vérifiez votre email** : Alpha Vantage vous enverra un email avec votre clé API
3. **Ouvrez l'email** (peut prendre quelques minutes)
4. **Copiez la clé API** depuis l'email
   - La clé ressemble à : `ABCD1234EFGH5678IJKL9012MNOP3456`

💡 **Note** : Si vous ne recevez pas l'email :
- Vérifiez vos spams
- Attendez 5-10 minutes
- Réessayez avec un autre email si nécessaire

#### Étape 4 : Comprendre les Limites (Gratuit)

**Plan Gratuit** :
- ✅ **5 appels API par minute**
- ✅ **500 appels par jour**
- ✅ **Données en temps réel**
- ✅ **Indicateurs techniques** (SMA, RSI, etc.)

⚠️ **Important** : Le projet gère automatiquement ces limites avec un système de cache et de rate limiting. Vous ne devriez pas avoir de problèmes si vous testez avec quelques tickers.

**Si vous dépassez les limites** :
- Attendez 1 minute pour réessayer
- Ou passez à un plan premium (payant)

---

## 3. Clé API OpenAI (Optionnel)

> **Note** : OpenAI est maintenant optionnel. Gemini est recommandé car il est gratuit.

Si vous préférez utiliser OpenAI au lieu de Gemini, suivez les étapes ci-dessous. Sinon, vous pouvez ignorer cette section.

### 🎯 Pourquoi OpenAI API ?

OpenAI API est nécessaire pour utiliser les modèles de langage (GPT-4o, GPT-3.5-turbo) qui alimentent l'agent financier et le système RAG.

### ✅ Étapes Détaillées

#### Étape 1 : Créer un Compte OpenAI

1. **Ouvrez votre navigateur** et allez sur : https://platform.openai.com/
2. **Cliquez sur "Sign up"** (S'inscrire) en haut à droite
3. **Remplissez le formulaire** :
   - Email
   - Mot de passe (minimum 8 caractères)
   - Acceptez les conditions d'utilisation
4. **Vérifiez votre email** : OpenAI vous enverra un email de confirmation
5. **Cliquez sur le lien** dans l'email pour confirmer votre compte

#### Étape 2 : Ajouter une Méthode de Paiement (Optionnel mais Recommandé)

⚠️ **Important** : Même si OpenAI offre des crédits gratuits, vous devrez peut-être ajouter une carte de crédit pour certaines fonctionnalités.

1. **Connectez-vous** à https://platform.openai.com/
2. **Cliquez sur votre profil** (icône en haut à droite)
3. **Sélectionnez "Billing"** (Facturation)
4. **Cliquez sur "Add payment method"** (Ajouter un moyen de paiement)
5. **Remplissez les informations** de votre carte bancaire
6. **Confirmez** l'ajout

💡 **Note** : OpenAI offre généralement **$5 de crédits gratuits** pour les nouveaux comptes, ce qui est suffisant pour tester le projet.

#### Étape 3 : Créer une Clé API

1. **Allez sur** : https://platform.openai.com/api-keys
   - Ou : Connectez-vous → Cliquez sur votre profil → "API keys"
2. **Cliquez sur "Create new secret key"** (Créer une nouvelle clé secrète)
3. **Donnez un nom** à votre clé (ex: "FinSight AI - Projet Portfolio")
4. **Cliquez sur "Create secret key"**
5. **⚠️ COPIEZ LA CLÉ IMMÉDIATEMENT** - Elle ne sera affichée qu'une seule fois !
   - La clé ressemble à : `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
6. **Collez-la dans un fichier texte temporaire** pour ne pas la perdre

---

## 4. Configuration dans le Projet

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

1. **Ouvrez le fichier `.env`** avec un éditeur de texte (Notepad, VS Code, etc.)
2. **Remplacez les valeurs** :

   ```env
   # Avant
   GEMINI_API_KEY=your_gemini_api_key_here
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here

   # Après (avec vos vraies clés)
   GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ALPHA_VANTAGE_API_KEY=ABCD1234EFGH5678IJKL9012MNOP3456
   ```

3. **Sauvegardez le fichier** (Ctrl+S ou Cmd+S)

### Étape 3 : Vérifier le Fichier .env

Votre fichier `.env` devrait ressembler à ceci :

```env
# API Keys
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
ALPHA_VANTAGE_API_KEY=votre_vraie_clé_alpha_vantage_ici

# Model Configuration
LLM_MODEL=gemini-pro
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
```

⚠️ **Sécurité** : 
- Ne partagez JAMAIS votre fichier `.env`
- Ne commitez JAMAIS votre fichier `.env` sur GitHub
- Le fichier est déjà dans `.gitignore` pour votre sécurité

---

## 5. Vérification

### Test Rapide des Clés

#### Tester la Clé Gemini

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
       response = model.generate_content("Hello")
       print("✅ Connexion Gemini réussie!")
       print(f"Réponse: {response.text}")
   else:
       print("❌ Clé Gemini non trouvée")
   ```

#### Tester la Clé Alpha Vantage

1. **Ouvrez un terminal Python** :
   ```bash
   python
   ```

2. **Testez la connexion** :
   ```python
   import os
   from dotenv import load_dotenv
   import requests

   load_dotenv()
   api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
   
   if api_key:
       print("✅ Clé Alpha Vantage trouvée")
       # Test simple
       url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey={api_key}"
       response = requests.get(url)
       if "Error Message" not in response.json():
           print("✅ Connexion Alpha Vantage réussie!")
       else:
           print("❌ Erreur:", response.json()["Error Message"])
   else:
       print("❌ Clé Alpha Vantage non trouvée")
   ```

### Test avec l'Application

1. **Lancez l'application** :
   ```bash
   streamlit run src/ui/dashboard.py
   ```

2. **Dans la sidebar**, vérifiez que les clés sont chargées :
   - Les champs ne devraient pas être vides
   - Si vous voyez vos clés (même partiellement), c'est bon signe

3. **Testez avec un ticker** :
   - Entrez `AAPL` dans le champ "Stock Ticker"
   - Cliquez sur "🚀 Lancer l'Analyse"
   - Si les données s'affichent, vos clés fonctionnent ! ✅

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

### Problème : "Rate limit exceeded" (Alpha Vantage)

**Solutions** :
1. Attendez 1 minute (limite de 5 appels/minute)
2. Le système gère automatiquement cela avec le cache
3. Si le problème persiste, vérifiez que vous n'avez pas dépassé 500 appels/jour

### Problème : Email Alpha Vantage non reçu

**Solutions** :
1. Vérifiez vos spams/courriers indésirables
2. Attendez 10-15 minutes
3. Réessayez avec un autre email
4. Contactez le support Alpha Vantage si nécessaire

---

## 📊 Résumé des Coûts

| Service | Coût | Limites Gratuites |
|---------|------|-------------------|
| **Gemini (Google)** | Gratuit | 60 req/min, 1500/jour |
| **Alpha Vantage** | Gratuit | 5 appels/min, 500/jour |
| **OpenAI** (Optionnel) | Payant | $5 crédits gratuits pour nouveaux comptes |

💡 **Estimation pour tester le projet** :
- **Gemini** : Gratuit, 1500 requêtes/jour = largement suffisant ! ✅
- **Alpha Vantage** : Gratuit, suffisant pour tester
- **OpenAI** : $5 de crédits gratuits = ~1000-5000 requêtes (si vous choisissez cette option)

---

## ✅ Checklist Finale

Avant de lancer l'application, vérifiez :

- [ ] Compte Google créé (pour Gemini)
- [ ] Clé API Gemini obtenue sur https://aistudio.google.com/app/apikey
- [ ] Clé API Alpha Vantage obtenue et copiée
- [ ] Fichier `.env` créé à la racine du projet
- [ ] Clés API ajoutées dans le fichier `.env` (GEMINI_API_KEY et ALPHA_VANTAGE_API_KEY)
- [ ] Fichier `.env` sauvegardé
- [ ] Test de connexion réussi (optionnel)

---

## 🎉 C'est Prêt !

Une fois vos clés configurées, vous pouvez lancer l'application :

```bash
streamlit run src/ui/dashboard.py
```

**Bon développement ! 🚀**

---

**Besoin d'aide ?** Consultez :
- [QUICKSTART.md](QUICKSTART.md) - Guide de démarrage rapide
- [GUIDE_EXECUTION.md](GUIDE_EXECUTION.md) - Guide d'installation complet
- [README.md](README.md) - Documentation principale

