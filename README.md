# 📊 FinSight AI - Plateforme d'Analyse Financière Intelligente

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![LlamaIndex](https://img.shields.io/badge/LlamaIndex-0.10.15-green.svg)](https://www.llamaindex.ai/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI/CD](https://github.com/ELMANDOURIHAMZA/FinSight-AI/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/ELMANDOURIHAMZA/FinSight-AI/actions)

> **🚀 Solution professionnelle d'analyse financière** alimentée par l'IA pour analyser les entreprises cotées en bourse, leurs rapports SEC 10-K et leurs données de marché en temps réel. **Interface intuitive, résultats précis, prêt pour la production.**
 
 **Important — Framework principal : Flask**
 
 L'application principale est une application **Flask** (point d'entrée `app.py`, script de démarrage `run_flask.py`). Démarrez localement avec :
 
 ```bash
 python run_flask.py
 ```
 
 Un tableau de bord Streamlit existe également sous `src/ui/dashboard.py` comme interface alternative ou version historique — il n'est pas utilisé par le serveur Flask par défaut.

## 🎯 Pourquoi FinSight AI ?

FinSight AI transforme l'analyse financière en rendant accessible l'analyse approfondie des entreprises cotées en bourse. Que vous soyez **investisseur**, **analyste financier**, ou **étudiant**, notre plateforme vous permet de :

- ✅ **Analyser rapidement** les rapports annuels de 100+ pages
- ✅ **Comprendre les risques** et opportunités en langage clair
- ✅ **Visualiser les données** de marché avec des graphiques professionnels
- ✅ **Poser des questions** en langage naturel et obtenir des réponses précises
- ✅ **Gagner du temps** : analyse complète en minutes au lieu d'heures

## 🎯 Vue d'ensemble

FinSight AI est un système d'analyse financière avancé qui combine :
- **RAG avancé** pour l'analyse de documents financiers volumineux (rapports SEC 10-K)
- **Agents autonomes** (pattern ReAct) pour raisonner et utiliser des outils
- **Intégration de données** en temps réel (Alpha Vantage API)
- **Interface interactive** (Streamlit) pour une expérience utilisateur fluide

### ✨ Fonctionnalités Professionnelles

#### 📈 Dashboard Marché Interactif
- **Visualisations en temps réel** : Graphiques professionnels avec indicateurs techniques (SMA, RSI, Volume)
- **Métriques clés** : Prix, capitalisation, ratio P/E, rendement dividende
- **Analyse technique** : Identification automatique des tendances et signaux
- **Interface moderne** : Design Analytics Dashboard professionnel

#### 💬 Assistant Financier IA
- **Questions en langage naturel** : Posez vos questions comme à un analyste
- **Réponses avec citations** : Chaque réponse cite les sections du rapport
- **Analyse combinée** : Combine données de marché et rapport 10-K
- **Contexte complet** : Utilise tout le rapport pour des réponses précises

#### 📄 Explorateur de Documents
- **Navigation intuitive** : Explorez les sections du rapport 10-K facilement
- **Recherche avancée** : Trouvez rapidement les informations pertinentes
- **Extraction intelligente** : Sections organisées et structurées

#### 🔍 Technologie de Pointe
- **RAG Avancé** : Recherche sémantique avec reranking
- **Agents Autonomes** : Pattern ReAct pour raisonnement complexe
- **Données Temps Réel** : Intégration API Alpha Vantage
- **Cache Intelligent** : Optimisation des performances

## 🏗️ Architecture

```
┌─────────────────┐
│   Streamlit UI  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────────┐
│  RAG  │ │  Agent    │
│System │ │  ReAct    │
└───┬───┘ └───┬───────┘
    │         │
    │    ┌────┴────┐
    │    │  Tools  │
    │    └────┬────┘
    │         │
┌───▼─────────▼───┐
│  Data Sources   │
│  - SEC EDGAR    │
│  - Alpha Vantage│
└─────────────────┘
```

### Stack Technologique

| Composant | Technologie | Justification |
|-----------|------------|---------------|
| **Langage** | Python 3.10+ | Standard en Data Science et IA |
| **Framework IA** | LlamaIndex | Spécialisé pour le RAG et la gestion de données |
| **LLM** | Google Gemini Pro | Gratuit, performances élevées |
| **Embeddings** | HuggingFace (BAAI/bge-small-en-v1.5) | Modèle open-source performant |
| **Vector DB** | ChromaDB | Légère, persistante, mode fichier local |
| **Interface** | Streamlit | Développement rapide d'UI en Python |
| **Données Bourse** | Alpha Vantage API | API robuste avec tier gratuit |
| **Données SEC** | sec-edgar-downloader | Wrapper efficace pour EDGAR |
| **Conteneurisation** | Docker | Reproducibilité et déploiement |

## 🚀 Démarrage Rapide

### ⚡ Installation en 3 Étapes

1. **Cloner le projet**
   ```bash
   git clone https://github.com/ELMANDOURIHAMZA/FinSight-AI.git
   cd FinSight-AI
   ```

2. **Installer les dépendances**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configurer et lancer**
   ```bash
   # Créer .env depuis env.template
   cp env.template .env
   # Éditer .env avec vos clés API
   streamlit run src/ui/dashboard.py
   ```

### 📋 Prérequis

- **Python 3.10+** (testé sur 3.11)
- **Clés API gratuites** :
  - 🔑 [Gemini API](https://aistudio.google.com/app/apikey) - Gratuit, 60 req/min
  - 🔑 [Alpha Vantage API](https://www.alphavantage.co/support/#api-key) - Gratuit, 5 req/min

> **📖 Guide détaillé** : Consultez **[GUIDE_GEMINI_API.md](GUIDE_GEMINI_API.md)** pour obtenir votre clé Gemini, ou **[GUIDE_CLES_API.md](GUIDE_CLES_API.md)** pour un guide complet de toutes les clés API.

### Installation Locale

1. **Cloner le repository**
```bash
git clone https://github.com/ELMANDOURIHAMZA/FinSight-AI.git
cd FinSight-AI
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**

Créez un fichier `.env` à la racine du projet :
```bash
cp env.template .env
```

Éditez `.env` et ajoutez vos clés API :
```env
GEMINI_API_KEY=your_gemini_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
LLM_MODEL=gemini-pro
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```

5. **Créer les répertoires de données**
```bash
mkdir -p data/raw data/vector_db
```

### Installation avec Docker

1. **Construire l'image Docker**
```bash
docker build -t finsight-ai .
```

2. **Lancer avec Docker Compose**
```bash
docker-compose up
```

L'application sera accessible sur `http://localhost:8501`

### Utilisation avec Make

```bash
# Installation
make install

# Lancer l'application
make run

# Lancer les tests
make test

# Linting
make lint

# Formatage du code
make format
```

## 📖 Guide d'Utilisation

### 1. Lancer l'Application

```bash
streamlit run src/ui/dashboard.py
```

Ou avec Make :
```bash
make run
```

### 2. Configuration Initiale

1. Ouvrez l'application dans votre navigateur (généralement `http://localhost:8501`)
2. Dans la sidebar, configurez vos clés API :
   - OpenAI API Key
   - Alpha Vantage API Key
3. Sélectionnez le modèle LLM (GPT-4o recommandé pour de meilleures performances)

### 3. Analyser une Entreprise

1. **Entrer un Ticker** : Dans la sidebar, entrez un symbole boursier (ex: `AAPL`, `MSFT`, `GOOGL`)
2. **Lancer l'Analyse** : Cliquez sur "🚀 Lancer l'Analyse"
3. **Explorer les Résultats** :
   - **Onglet Dashboard Marché** : Visualisez les graphiques et métriques financières
   - **Onglet Assistant Financier** : Posez des questions sur le rapport 10-K
   - **Onglet Explorateur de Documents** : Parcourez les sections du rapport

### 4. Exemples de Questions pour l'Assistant

- *"Quels sont les principaux risques identifiés dans le rapport?"*
- *"Quelle est la stratégie de croissance de l'entreprise?"*
- *"Compare le sentiment du rapport avec la performance boursière récente"*
- *"Quels sont les facteurs de risque liés au changement climatique?"*
- *"L'action est-elle surévaluée par rapport aux risques mentionnés?"*

## 🧪 Tests

### Lancer les Tests

```bash
# Tous les tests
pytest tests/ -v

# Avec couverture de code
pytest tests/ -v --cov=src --cov-report=html

# Tests spécifiques
pytest tests/test_alpha_vantage.py -v
```

### Structure des Tests

- `tests/test_alpha_vantage.py` : Tests du client Alpha Vantage
- `tests/test_sec_edgar.py` : Tests du client SEC EDGAR
- `tests/test_rag.py` : Tests du système RAG
- `tests/conftest.py` : Configuration et fixtures pytest

## 📊 Évaluation du RAG

Le projet intègre [RAGAS](https://github.com/explodinggradients/ragas) pour l'évaluation quantitative de la qualité des réponses RAG.

### Métriques Évaluées

- **Faithfulness** : La réponse respecte-t-elle le contexte source ?
- **Context Recall** : Le système a-t-il trouvé toute l'information nécessaire ?
- **Answer Relevance** : La réponse est-elle pertinente par rapport à la question ?

### Exemple d'Utilisation

```python
from ragas import evaluate
from ragas.metrics import faithfulness, context_recall

# Dataset de validation
dataset = {
    "question": ["Quels sont les risques climatiques?"],
    "answer": ["Les risques incluent..."],
    "contexts": [["Extrait du rapport..."]],
    "ground_truth": ["Réponse attendue..."]
}

# Évaluation
results = evaluate(dataset, metrics=[faithfulness, context_recall])
print(results)
```

## 🐳 Déploiement

### Streamlit Cloud

1. Poussez votre code sur GitHub
2. Connectez-vous à [Streamlit Cloud](https://streamlit.io/cloud)
3. Importez votre repository
4. Configurez les secrets (clés API) dans les paramètres
5. Déployez !

### Hugging Face Spaces

1. Créez un nouveau Space sur [Hugging Face](https://huggingface.co/spaces)
2. Sélectionnez "Docker" comme SDK
3. Poussez votre code avec le Dockerfile
4. Configurez les secrets dans les paramètres

## 📁 Structure du Projet

```
FinSight-AI/
├── .github/
│   └── workflows/
│       └── ci_cd.yml          # Pipeline CI/CD
├── data/                       # Données (ignoré par Git)
│   ├── raw/                    # Fichiers bruts (PDFs, JSONs)
│   └── vector_db/              # Base de données vectorielle ChromaDB
├── src/
│   ├── agents/                 # Logique des agents
│   │   ├── finance_agent.py   # Agent ReAct principal
│   │   └── tools.py            # Outils pour l'agent
│   ├── data/                   # Accès aux données
│   │   ├── alpha_vantage.py    # Client API Bourse
│   │   └── sec_edgar.py        # Client API SEC + Parsing
│   ├── rag/                    # Moteur RAG
│   │   ├── ingestion.py        # Chunking & Indexation
│   │   └── retrieval.py        # Configuration du Retriever
│   └── ui/                     # Composants Streamlit
│       └── dashboard.py         # Application principale
├── tests/                      # Tests unitaires
├── .env.example                # Modèle de variables d'environnement
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── pyproject.toml
├── requirements.txt
└── README.md
```

## 🔧 Développement

### Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche pour votre feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Standards de Code

- **Formatage** : Utilisez `black` (configuré dans `pyproject.toml`)
- **Linting** : Utilisez `flake8` (max line length: 100)
- **Tests** : Assurez-vous que tous les tests passent avant de commit

```bash
make format  # Formater le code
make lint    # Vérifier le style
make test    # Lancer les tests
```

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- [LlamaIndex](https://www.llamaindex.ai/) pour le framework RAG
- [Alpha Vantage](https://www.alphavantage.co/) pour l'API de données boursières
- [SEC EDGAR](https://www.sec.gov/edgar.shtml) pour l'accès aux rapports financiers
- [Streamlit](https://streamlit.io/) pour le framework UI

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.

---

**Développé avec ❤️ pour démontrer l'excellence en IA et Data Science**

