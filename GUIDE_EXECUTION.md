# 📘 Guide d'Exécution Pas à Pas - FinSight AI

Ce guide vous accompagne étape par étape pour installer, configurer et exécuter FinSight AI sur votre machine.

## 📋 Table des Matières

1. [Prérequis](#prérequis)
2. [Installation sur Windows](#installation-sur-windows)
3. [Installation sur Linux/Mac](#installation-sur-linuxmac)
4. [Installation avec Docker](#installation-avec-docker)
5. [Configuration](#configuration)
6. [Premier Lancement](#premier-lancement)
7. [Utilisation](#utilisation)
8. [Dépannage](#dépannage)

---

## 📋 Prérequis

### Logiciels Requis

- **Python 3.10 ou supérieur** : [Télécharger Python](https://www.python.org/downloads/)
- **Git** : [Télécharger Git](https://git-scm.com/downloads)
- **Clés API** :
  - [OpenAI API Key](https://platform.openai.com/api-keys) (payant, mais crédits gratuits disponibles)
  - [Alpha Vantage API Key](https://www.alphavantage.co/support/#api-key) (gratuit)

### Vérification des Prérequis

Ouvrez un terminal et vérifiez :

```bash
python --version  # Doit afficher Python 3.10 ou supérieur
git --version     # Doit afficher une version de Git
```

---

## 🪟 Installation sur Windows

### Étape 1 : Cloner le Repository

```powershell
# Ouvrir PowerShell dans le répertoire souhaité
cd Desktop
git clone https://github.com/ELMANDOURIHAMZA/FinSight-AI.git
cd "FinSight-AI - Agent Financier Autonome"
```

### Étape 2 : Créer un Environnement Virtuel

```powershell
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1
```

**Note** : Si vous obtenez une erreur d'exécution de script, exécutez :
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Étape 3 : Installer les Dépendances

```powershell
# Mettre à jour pip
python -m pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt
```

Cette étape peut prendre 5-10 minutes selon votre connexion internet.

### Étape 4 : Créer les Répertoires de Données

```powershell
# Créer les dossiers nécessaires
New-Item -ItemType Directory -Force -Path data\raw, data\vector_db
```

---

## 🐧 Installation sur Linux/Mac

### Étape 1 : Cloner le Repository

```bash
cd ~/Desktop
git clone https://github.com/ELMANDOURIHAMZA/FinSight-AI.git
cd "FinSight-AI - Agent Financier Autonome"
```

### Étape 2 : Créer un Environnement Virtuel

```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate
```

### Étape 3 : Installer les Dépendances

```bash
# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt
```

### Étape 4 : Créer les Répertoires de Données

```bash
mkdir -p data/raw data/vector_db
```

---

## 🐳 Installation avec Docker

### Étape 1 : Installer Docker

- **Windows/Mac** : [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux** : Suivez les [instructions officielles](https://docs.docker.com/engine/install/)

### Étape 2 : Cloner le Repository

```bash
git clone https://github.com/ELMANDOURIHAMZA/FinSight-AI.git
cd "FinSight-AI - Agent Financier Autonome"
```

### Étape 3 : Créer le Fichier .env

Créez un fichier `.env` à la racine du projet :

```env
OPENAI_API_KEY=your_openai_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
```

### Étape 4 : Construire et Lancer

```bash
# Construire l'image
docker-compose build

# Lancer le conteneur
docker-compose up
```

L'application sera accessible sur `http://localhost:8501`

---

## ⚙️ Configuration

### Étape 1 : Obtenir les Clés API

#### OpenAI API Key

1. Allez sur [platform.openai.com](https://platform.openai.com/)
2. Créez un compte ou connectez-vous
3. Allez dans "API keys"
4. Cliquez sur "Create new secret key"
5. Copiez la clé (elle ne sera affichée qu'une seule fois !)

#### Alpha Vantage API Key

1. Allez sur [alphavantage.co](https://www.alphavantage.co/support/#api-key)
2. Remplissez le formulaire avec votre email
3. Vous recevrez la clé par email (gratuit, pas de carte de crédit requise)

### Étape 2 : Configurer le Fichier .env

1. **Copiez le fichier exemple** :
   ```bash
   # Windows PowerShell
   Copy-Item env.template .env
   
   # Linux/Mac
   cp env.template .env
   ```

2. **Ouvrez `.env` avec un éditeur de texte** et remplacez :
   ```env
   OPENAI_API_KEY=votre_clé_openai_ici
   ALPHA_VANTAGE_API_KEY=votre_clé_alpha_vantage_ici
   LLM_MODEL=gpt-4o
   EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
   ```

3. **Sauvegardez le fichier**

**⚠️ Important** : Ne partagez jamais votre fichier `.env` ! Il est déjà dans `.gitignore`.

---

## 🚀 Premier Lancement

### Méthode 1 : Avec Streamlit (Recommandé)

```bash
# Assurez-vous que l'environnement virtuel est activé
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate

# Lancer l'application
streamlit run src/ui/dashboard.py
```

### Méthode 2 : Avec Make

```bash
# Si vous avez Make installé
make run
```

### Résultat Attendu

1. Une fenêtre de terminal s'ouvre avec des logs
2. Votre navigateur s'ouvre automatiquement sur `http://localhost:8501`
3. Si le navigateur ne s'ouvre pas, copiez-collez l'URL affichée dans le terminal

---

## 💡 Utilisation

### Interface Utilisateur

L'application se compose de 3 onglets principaux :

#### 1. 📈 Dashboard Marché

1. **Entrez un ticker** dans la sidebar (ex: `AAPL`, `MSFT`, `GOOGL`)
2. **Cliquez sur "🚀 Lancer l'Analyse"**
3. **Visualisez** :
   - Prix actuel et métriques clés
   - Graphique interactif avec SMA et RSI
   - Informations sur l'entreprise

#### 2. 💬 Assistant Financier

1. **Lancez d'abord l'analyse** dans l'onglet Dashboard
2. **Attendez** que le rapport 10-K soit chargé (première fois uniquement)
3. **Posez des questions** dans le chat, par exemple :
   - "Quels sont les principaux risques identifiés?"
   - "Quelle est la stratégie de croissance?"
   - "Compare le sentiment du rapport avec la performance boursière"

#### 3. 📄 Explorateur de Documents

- Parcourez les sections du rapport 10-K
- Visualisez le contenu brut des documents

### Exemples de Questions

**Questions sur les Risques** :
- "Quels sont les risques liés au changement climatique?"
- "Quels sont les principaux risques opérationnels?"

**Questions sur la Stratégie** :
- "Quelle est la stratégie de croissance de l'entreprise?"
- "Quels sont les principaux marchés cibles?"

**Questions Comparatives** :
- "L'action est-elle surévaluée par rapport aux risques?"
- "Compare la performance boursière avec les perspectives du rapport"

---

## 🔧 Dépannage

### Problème : "ModuleNotFoundError"

**Solution** : Vérifiez que l'environnement virtuel est activé et que les dépendances sont installées :
```bash
pip install -r requirements.txt
```

### Problème : "OPENAI_API_KEY not found"

**Solution** : Vérifiez que le fichier `.env` existe et contient votre clé API.

### Problème : "Rate limit exceeded" (Alpha Vantage)

**Solution** : L'API gratuite limite à 5 appels/minute. Le système gère automatiquement cela avec un cache. Attendez quelques minutes ou utilisez un compte premium.

### Problème : "Port 8501 already in use"

**Solution** : Un autre processus utilise le port. Soit :
- Arrêtez l'autre processus
- Ou changez le port : `streamlit run src/ui/dashboard.py --server.port 8502`

### Problème : Erreur lors du téléchargement du 10-K

**Solution** : 
- Vérifiez votre connexion internet
- Le téléchargement peut prendre plusieurs minutes pour les gros rapports
- Vérifiez que le ticker existe (ex: `AAPL` pour Apple, pas `APPLE`)

### Problème : L'application ne répond pas

**Solution** :
1. Vérifiez les logs dans le terminal
2. Assurez-vous que toutes les clés API sont valides
3. Redémarrez l'application

### Problème : Erreur ChromaDB

**Solution** : Supprimez le dossier `data/vector_db` et relancez :
```bash
# Windows
Remove-Item -Recurse -Force data\vector_db
New-Item -ItemType Directory -Path data\vector_db

# Linux/Mac
rm -rf data/vector_db
mkdir -p data/vector_db
```

---

## 📊 Vérification de l'Installation

Pour vérifier que tout fonctionne correctement :

```bash
# Lancer les tests
pytest tests/ -v

# Vérifier le linting
flake8 src/ --max-line-length=100
```

---

## 🆘 Support

Si vous rencontrez des problèmes :

1. **Vérifiez les logs** dans le terminal
2. **Consultez la section Dépannage** ci-dessus
3. **Ouvrez une issue** sur GitHub avec :
   - Votre système d'exploitation
   - La version de Python
   - Le message d'erreur complet
   - Les étapes pour reproduire le problème

---

## 🎉 Félicitations !

Vous êtes maintenant prêt à utiliser FinSight AI ! Explorez les fonctionnalités et n'hésitez pas à expérimenter avec différents tickers et questions.

**Bon analyse ! 📊🚀**

