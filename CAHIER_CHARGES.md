# 📋 Cahier des Charges Technique et Stratégique

## FinSight AI - Agent Financier Autonome

> **Version** : 1.0  
> **Date** : Décembre 2024  
> **Auteur** : Projet Portfolio GitHub

---

## 📑 Table des Matières

1. [Introduction et Vision Stratégique](#1-introduction-et-vision-stratégique)
2. [Analyse du Domaine et Cadre Théorique](#2-analyse-du-domaine-et-cadre-théorique)
3. [Spécifications Fonctionnelles](#3-spécifications-fonctionnelles)
4. [Architecture Technique Détaillée](#4-architecture-technique-détaillée)
5. [Ingénierie des Données et Stratégie ETL](#5-ingénierie-des-données-et-stratégie-etl)
6. [Développement du Cœur RAG et Agent](#6-développement-du-cœur-rag-et-agent)
7. [Assurance Qualité et Tests](#7-assurance-qualité-et-tests)
8. [Déploiement et Opérations (MLOps)](#8-déploiement-et-opérations-mlops)
9. [Valorisation Professionnelle](#9-valorisation-professionnelle)

---

## 1. Introduction et Vision Stratégique

### 1.1. Contexte du Marché de l'Emploi en IA et Data Science (2025)

L'année 2025 marque un tournant décisif dans le recrutement des profils technologiques liés à la donnée. La démocratisation des outils d'Intelligence Artificielle Générative (GenAI) a radicalement élevé les attentes des recruteurs. Il ne suffit plus de savoir importer une bibliothèque comme Pandas ou Scikit-Learn pour prétendre à un poste de Data Scientist ou d'Ingénieur IA.

Les entreprises recherchent désormais des profils hybrides, capables de :
- Comprendre les fondements théoriques des modèles de langage (LLMs)
- Intégrer ces modèles dans des architectures logicielles robustes
- Créer de la valeur métier concrète

Dans ce contexte, le portfolio GitHub d'un candidat doit devenir une vitrine de compétences "Full-Stack Data Science", démontrant une maîtrise de la chaîne de valeur complète : de l'acquisition de la donnée brute à son déploiement en production, en passant par l'orchestration complexe d'agents autonomes.

### 1.2. Définition du Projet "FinSight AI"

"FinSight AI" est un agent d'analyse financière autonome. Contrairement à un simple tableau de bord statique, cet agent est conçu pour agir comme un analyste junior virtuel. Il est capable d'ingérer des données hétérogènes — structurées (séries temporelles boursières) et non structurées (rapports annuels SEC 10-K, transcriptions d'appels aux investisseurs) — pour fournir des synthèses, répondre à des questions complexes et détecter des signaux faibles.

**Pertinence du projet** : La finance est un domaine où l'hallucination d'un modèle de langage est inacceptable. Construire un système capable de citer ses sources avec précision tout en analysant des tendances numériques démontre une rigueur technique supérieure.

### 1.3. Objectifs Pédagogiques et Professionnels

| Domaine de Compétence | Objectifs Spécifiques | Technologies Clés |
|----------------------|----------------------|-------------------|
| **Data Engineering** | Pipelines ETL robustes, gestion des limites d'API, nettoyage HTML/XBRL | Python, Pandas, Alpha Vantage API, SEC EDGAR API |
| **GenAI & RAG** | Architecture RAG avancée (indexation vectorielle, reranking, synthèse) | LlamaIndex, OpenAI/Gemini, ChromaDB |
| **Agentic AI** | Agents autonomes avec Function Calling | LlamaIndex Agents, ReAct Pattern |
| **Développement Logiciel** | Code modulaire, gestion des environnements, conteneurisation | Docker, Git, Streamlit, Poetry |
| **MLOps & Qualité** | Tests unitaires, évaluation quantitative (RAG Evaluation) | Pytest, RAGAS, GitHub Actions |

---

## 2. Analyse du Domaine et Cadre Théorique

### 2.1. Les Défis de l'Analyse Financière Automatisée

**Hétérogénéité des données** : Les rapports financiers mélangent texte dense, tableaux financiers complexes et notes de bas de page cruciales.

**Volatilité temporelle** : Une information financière est périssable. Le système doit distinguer les données historiques (rapport 2023) des données temps réel (cours de bourse actuel).

**Exigence de précision** : Une erreur sur un chiffre (ex: confondre "Revenu net" et "Revenu brut") est critique. Le système doit privilégier la fidélité ("Faithfulness") sur la créativité.

### 2.2. Fondements du RAG (Retrieval-Augmented Generation)

**Architecture Vectorielle** :
- Découpage en "chunks"
- Conversion en vecteurs via un modèle d'embedding
- Recherche par similarité cosinus

**RAG Naïf vs RAG Avancé** :
- **Hybrid Search** : Combinaison recherche vectorielle + BM25
- **Reranking** : Réordonnancement des résultats
- **Metadata Filtering** : Filtrage par année/entreprise

### 2.3. L'Approche Agentique (Agentic AI)

**Pattern ReAct (Reason + Act)** : L'agent analyse la demande, formule une pensée, exécute une action via un outil, observe le résultat, et itère jusqu'à la réponse finale.

**Utilisation d'Outils** : L'agent dispose d'outils spécifiques (FinancialReportTool, MarketDataTool) pour une modularité essentielle.

---

## 3. Spécifications Fonctionnelles

### 3.1. Profils Utilisateurs (Personas)

**Nom** : Alex  
**Rôle** : Analyste Financier Junior ou Investisseur Particulier Averti  
**Besoin** : Analyser rapidement plusieurs entreprises par jour, submergé par la longueur des rapports 10-K (+100 pages)  
**Compétence Technique** : Moyenne, besoin d'une interface graphique intuitive

### 3.2. Histoires Utilisateurs (User Stories)

| ID | Module | Priorité | Description | Critère d'Acceptation |
|----|--------|----------|-------------|----------------------|
| US-01 | Setup | P0 | Configurer les clés API | Les clés sont chargées sans erreur |
| US-02 | Data | P1 | Entrer un symbole boursier pour récupérer les données | Le système télécharge le 10-K et les cours sans plantage |
| US-03 | Market | P1 | Visualiser l'évolution du cours avec indicateurs techniques | Graphique interactif avec prix et SMA |
| US-04 | Chat | P1 | Poser une question sur le rapport annuel | Réponse cohérente et pertinente |
| US-05 | Proof | P2 | Voir les sources utilisées par l'IA | Les "Source Nodes" sont affichés |
| US-06 | Agent | P2 | Poser une question mixte (rapport + bourse) | L'agent utilise conjointement les outils |
| US-07 | Export | P3 | Télécharger un rapport PDF récapitulatif | Fichier PDF structuré généré |

### 3.3. Ergonomie et Interface (Streamlit)

**Sidebar** :
- Champ de saisie pour la clé API OpenAI
- Sélecteur de modèle (GPT-3.5-Turbo vs GPT-4o)
- Zone de recherche du Ticker
- Bouton "Lancer l'Analyse"

**Zone Principale - Onglets** :
- **Tab 1** : Dashboard Marché (Graphiques, KPIs)
- **Tab 2** : Assistant Financier (Chat)
- **Tab 3** : Explorateur de Documents

---

## 4. Architecture Technique Détaillée

### 4.1. Diagramme de Flux de Données

```
Utilisateur → Ticker → Orchestrateur ETL
    ↓
Cache Local ? → Oui : Charger
    ↓ Non
Alpha Vantage API → Prix
SEC EDGAR API → 10-K
    ↓
Parsing HTML → Chunking → Embeddings → ChromaDB
    ↓
Utilisateur → Question → AgentRunner
    ↓
RAG Tool / Market Tool → LLM Synthesis → Réponse
    ↓
Streamlit UI
```

### 4.2. Stack Technologique

| Composant | Technologie | Justification |
|-----------|------------|---------------|
| Langage | Python 3.10+ | Standard en Data Science |
| Framework IA | LlamaIndex | Spécialisé pour le RAG |
| LLM | OpenAI (GPT-4o) | Fiabilité et facilité |
| Embedding | HuggingFace (BAAI/bge-small-en-v1.5) | Open source, local |
| Vector DB | ChromaDB | Légère, mode fichier local |
| Interface | Streamlit | UI interactive en Python |
| Données Bourse | Alpha Vantage | API robuste, tier gratuit |
| Données SEC | sec-edgar-api | Wrapper efficace |
| Ops | Docker | Conteneurisation |

### 4.3. Structure du Répertoire

```
FinSight-AI/
├── .github/workflows/ci_cd.yml
├── data/raw/ & vector_db/
├── src/
│   ├── agents/ (finance_agent.py, tools.py)
│   ├── data/ (alpha_vantage.py, sec_edgar.py)
│   ├── rag/ (ingestion.py, retrieval.py)
│   └── ui/ (dashboard.py)
├── tests/
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── pyproject.toml
└── README.md
```

---

## 5. Ingénierie des Données et Stratégie ETL

### 5.1. Gestion de l'API Alpha Vantage (Rate Limiting)

**Stratégie** :
- Décorateur de caching (functools.lru_cache ou persistance disque)
- Gestionnaire de Rate Limit (Token Bucket)
- Backoff exponentiel
- Batching des appels

**Limites** : 5 requêtes/minute, 500/jour (tier gratuit)

### 5.2. Pipeline d'Ingestion des Rapports SEC (10-K)

**Étapes** :
1. Identification via sec-edgar-api (CIK)
2. Nettoyage HTML avec BeautifulSoup
3. Chunking sémantique (SentenceSplitter)
4. Taille recommandée : 1024 tokens, overlap 200 tokens

### 5.3. Base de Données Vectorielle (ChromaDB)

- Mode persistent dans `data/vector_db`
- Permet de relancer sans ré-indexation
- Économise les coûts d'embedding

---

## 6. Développement du Cœur RAG et Agent

### 6.1. Configuration de LlamaIndex

- **LLM** : OpenAI(model="gpt-4o", temperature=0)
- **Embedding** : HuggingFaceEmbedding("BAAI/bge-small-en-v1.5")

### 6.2. Création des Outils (Tools)

**Outil 1** : `analyze_10k_report` (RAG)  
**Outil 2** : `get_stock_metrics` (Market Data)

### 6.3. Implémentation de l'Agent ReAct

```python
agent = ReActAgent.from_tools(
    [finance_tool, market_tool],
    llm=llm,
    verbose=True,
    system_prompt="You are an expert financial analyst..."
)
```

### 6.4. Prompt Engineering

Le system_prompt doit instruire l'agent sur :
- Le ton : Professionnel, neutre, objectif
- Le format : Structuré, Markdown
- La gestion de l'inconnu : "Je ne sais pas" plutôt qu'inventer

---

## 7. Assurance Qualité et Tests

### 7.1. Tests Unitaires (Pytest)

- Test ETL : Mocker l'API Alpha Vantage
- Test Parsing : Fichier HTML fictif
- Commande : `pytest tests/` doit passer avant commit

### 7.2. Évaluation du RAG (RAGAS)

**Dataset de validation** : 10 paires (Question, Réponse Attendue, Contexte)

**Métriques** :
- **Faithfulness** : La réponse respecte-t-elle le contexte?
- **Context Recall** : Toute l'information nécessaire a-t-elle été trouvée?

### 7.3. Gestion des Dépendances

- `requirements.txt` propre
- Versions pinées pour reproductibilité
- Séparation dev/prod si possible

---

## 8. Déploiement et Opérations (MLOps)

### 8.1. Conteneurisation (Docker)

Dockerfile optimisé avec :
- Python 3.10-slim
- Installation des dépendances système
- Cache des layers Docker
- Exposition du port 8501

### 8.2. CI/CD (GitHub Actions)

Workflow `.github/workflows/ci_cd.yml` :
- Checkout
- Installation Python
- Linting (Flake8)
- Tests (Pytest)
- Build Docker

### 8.3. Hébergement

- **Streamlit Cloud** : Solution la plus simple
- **Hugging Face Spaces** : Alternative gratuite avec Docker

---

## 9. Valorisation Professionnelle

### 9.1. Le README.md "Parfait"

- Titre & Accroche accrocheur
- Badges (Python, LlamaIndex, Docker, CI/CD)
- Demo GIF
- Architecture Diagram (Mermaid.js)
- Features claires
- Getting Started (3 lignes de commande)
- Evaluation (scores RAGAS)

### 9.2. Stratégie de Contenu LinkedIn

**Modèle de Post Viral (AIDA)** :
- **Attention** : Hook accrocheur
- **Intérêt** : Description du problème résolu
- **Désir** : Détails techniques (RAG, rate limiting, XBRL)
- **Action** : Lien GitHub, recherche de poste

**Hashtags** : #LlamaIndex #RAG #AIAnalysis #FinTech #Python #OpenToWork

### 9.3. Réseautage Ciblé

Message court aux Lead Data Scientists :
- Présentation du projet
- Demande de feedback technique
- Lien GitHub

---

## 10. Timeline Suggérée

- **Semaine 1** : Data Engineering (Alpha Vantage, SEC Parsing)
- **Semaine 2** : Core RAG & LlamaIndex implementation
- **Semaine 3** : Interface Streamlit & Agent Logic
- **Semaine 4** : Docker, Tests, Documentation et Lancement LinkedIn

---

## Conclusion

Ce cahier des charges offre une feuille de route complète pour passer d'un statut d'étudiant à celui de professionnel confirmé. Le projet "FinSight AI" couvre l'ensemble du spectre attendu en 2025 : de la donnée brute à l'agent intelligent, du code local au déploiement cloud.

En suivant cette rigueur, le dépôt GitHub deviendra un atout indéniable, prouvant non seulement une compétence technique, mais une capacité à délivrer de la valeur métier concrète.

---

**Document Version** : 1.0  
**Dernière Mise à Jour** : Décembre 2024






