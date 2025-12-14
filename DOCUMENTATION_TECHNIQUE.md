# 📚 Documentation Technique Complète - FinSight AI

> **Documentation exhaustive** de tous les aspects techniques du projet FinSight AI  
> **Version** : 1.0 | **Date** : Décembre 2024

---

## 📑 Table des Matières

1. [Vue d'Ensemble Architecturale](#1-vue-densemble-architecturale)
2. [Modèles et Technologies IA](#2-modèles-et-technologies-ia)
3. [Architecture des Données](#3-architecture-des-données)
4. [Architecture Logicielle](#4-architecture-logicielle)
5. [Détails d'Implémentation du Code](#5-détails-dimplémentation-du-code)
6. [Patterns de Design](#6-patterns-de-design)
7. [Flux de Données et Processus](#7-flux-de-données-et-processus)
8. [Optimisations et Performance](#8-optimisations-et-performance)
9. [Gestion des Erreurs et Résilience](#9-gestion-des-erreurs-et-résilience)
10. [Sécurité et Bonnes Pratiques](#10-sécurité-et-bonnes-pratiques)

---

## 1. Vue d'Ensemble Architecturale

### 1.1. Architecture Système Global

```
┌─────────────────────────────────────────────────────────────┐
│                      STREAMLIT UI LAYER                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ Dashboard│  │  Chat UI │  │ Explorer │                  │
│  │  Marché  │  │ Assistant│  │ Documents│                  │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘                  │
└────────┼──────────────┼──────────────┼───────────────────────┘
         │              │              │
         └──────────────┴──────────────┘
                        │
         ┌──────────────┴──────────────┐
         │     ORCHESTRATION LAYER      │
         │  (dashboard.py - main logic) │
         └──────────────┬───────────────┘
                        │
    ┌───────────────────┴───────────────────┐
    │                                       │
┌───▼──────────────┐            ┌──────────▼──────────┐
│   AGENT LAYER    │            │    RAG LAYER        │
│  (ReAct Pattern) │            │ (Vector Search)     │
│                  │            │                     │
│  ┌────────────┐  │            │  ┌──────────────┐  │
│  │FinanceAgent│  │            │  │Document      │  │
│  └─────┬──────┘  │            │  │Ingester      │  │
│        │         │            │  └──────┬───────┘  │
│  ┌─────▼─────┐   │            │         │          │
│  │   Tools   │   │            │  ┌──────▼───────┐  │
│  │  - RAG    │   │            │  │AdvancedRAG   │  │
│  │  - Market │   │            │  │Retriever     │  │
│  └───────────┘   │            │  └──────────────┘  │
└──────────────────┘            └────────────────────┘
         │                              │
         └──────────┬───────────────────┘
                    │
         ┌──────────▼──────────┐
         │   DATA LAYER        │
         │                     │
         │  ┌──────────────┐   │
         │  │Alpha Vantage │   │
         │  │API Client    │   │
         │  └──────┬───────┘   │
         │         │           │
         │  ┌──────▼───────┐   │
         │  │SEC EDGAR     │   │
         │  │Client        │   │
         │  └──────┬───────┘   │
         │         │           │
         │  ┌──────▼───────┐   │
         │  │ChromaDB      │   │
         │  │Vector Store  │   │
         │  └──────────────┘   │
         └─────────────────────┘
```

### 1.2. Stack Technologique Complète

| Couche | Composant | Version | Justification Technique |
|--------|-----------|---------|------------------------|
| **Langage** | Python | 3.10+ | Standard pour Data Science, support natif asyncio, type hints |
| **Framework IA** | LlamaIndex | 0.10.15+ | Framework spécialisé RAG, abstraction des LLMs, agents |
| **LLM** | Google Gemini | models/gemini-2.0-flash-exp | Gratuit, performances élevées, support multimodal futur |
| **Embeddings** | HuggingFace BGE | bge-small-en-v1.5 | 384 dimensions, optimisé pour similarité sémantique |
| **Vector DB** | ChromaDB | 0.4.22+ | Base de données vectorielle légère, persistante, mode fichier |
| **Interface** | Streamlit | 1.31.0+ | Framework UI rapide, intégration Python native |
| **Données Bourse** | Alpha Vantage API | REST API | Données temps réel et historiques, tier gratuit |
| **Données SEC** | sec-edgar-downloader | 5.0.0+ | Wrapper Python pour API SEC EDGAR |
| **Parsing HTML** | BeautifulSoup4 + lxml | 4.12.0+ | Extraction et nettoyage de contenu HTML/XBRL |
| **Visualisation** | Plotly | 5.18.0+ | Graphiques interactifs, support technique indicators |
| **Data Processing** | Pandas + NumPy | 2.2.0+ | Manipulation données structurées, calculs numériques |
| **Conteneurisation** | Docker | Latest | Reproducibilité, déploiement isolé |
| **CI/CD** | GitHub Actions | - | Automatisation tests, linting, déploiement |

---

## 2. Modèles et Technologies IA

### 2.1. Modèle de Langage (LLM)

#### Configuration Gemini

```python
# Modèle utilisé : models/gemini-2.0-flash-exp
LLM = Gemini(
    model="models/gemini-2.0-flash-exp",
    temperature=0,  # Déterminisme maximal pour réponses financières
    api_key=api_key
)
```

**Caractéristiques techniques :**
- **Architecture** : Transformer-based, optimisé pour la génération
- **Contexte** : ~1M tokens (très large)
- **Temperature** : 0 (déterministe, crucial pour données financières)
- **Latence** : ~200-500ms par requête
- **Coût** : Gratuit avec limites (60 req/min, 1500 req/jour)

**Choix du modèle :**
- `gemini-2.0-flash-exp` : Modèle expérimental mais fonctionnel avec l'API actuelle
- Alternative : `gemini-1.5-pro` (si disponible) pour meilleures performances
- Fallback automatique implémenté dans le code

### 2.2. Modèle d'Embeddings

#### HuggingFace BGE-small-en-v1.5

```python
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)
```

**Spécifications techniques :**
- **Architecture** : BERT-based encoder
- **Dimensions** : 384 (équilibre précision/efficacité)
- **Taille** : ~134M paramètres
- **Vocabulaire** : 21128 tokens
- **Performance** : MTEB score 63.23 (excellent pour sa taille)
- **Latence** : ~10-50ms par chunk (CPU), <5ms (GPU)

**Avantages :**
- Exécution locale (pas de coût API)
- Modèle compact (téléchargement ~500MB)
- Optimisé pour similarité cosinus
- Support multilingue (principalement anglais)

### 2.3. Base de Données Vectorielle

#### ChromaDB

```python
chroma_client = chromadb.PersistentClient(
    path="data/vector_db",
    settings=ChromaSettings(anonymized_telemetry=False)
)
```

**Architecture :**
- **Type** : Base de données vectorielle in-memory avec persistance
- **Algorithme de recherche** : HNSW (Hierarchical Navigable Small World)
- **Distance** : Similarité cosinus par défaut
- **Indexation** : Automatique lors de l'insertion
- **Persistance** : SQLite + fichiers binaires

**Paramètres de configuration :**
- `similarity_top_k=5` : Nombre de chunks récupérés
- `similarity_cutoff=0.7` : Seuil minimal de similarité
- Collection par ticker : `finsight_{ticker}` pour isolation

---

## 3. Architecture des Données

### 3.1. Pipeline ETL - Alpha Vantage

```python
class AlphaVantageClient:
    BASE_URL = "https://www.alphavantage.co/query"
    
    # Rate Limiting: Token Bucket Algorithm
    @rate_limited(max_per_minute=5)
    def _make_request(self, params: Dict) -> Dict:
        # Limite: 5 req/min, 500 req/jour (tier gratuit)
```

**Flux de données :**

```
User Request → Cache Check → API Call (if needed) → 
Rate Limiting → Response → Cache Save → Return Data
```

**Stratégie de cache :**
- **Durée** : Cache quotidien (fichier par jour)
- **Format** : JSON dans `data/raw/{symbol}_{function}_{date}.json`
- **Invalidation** : Automatique (nouveau fichier chaque jour)
- **Espace disque** : ~50KB par ticker par jour

**Endpoints utilisés :**
1. `GLOBAL_QUOTE` : Prix actuel, volume, variations
2. `TIME_SERIES_DAILY` : Historique prix (compact: 100 jours, full: 20 ans)
3. `OVERVIEW` : Données fondamentales (PE, market cap, etc.)

### 3.2. Pipeline ETL - SEC EDGAR

```python
class SecEdgarClient:
    def get_10k_text(self, ticker: str) -> Dict[str, str]:
        # 1. Convert ticker → CIK
        # 2. Download 10-K HTML
        # 3. Parse sections
        # 4. Cache result
```

**Flux de traitement :**

```
Ticker → CIK Mapping → SEC API → Download HTML → 
BeautifulSoup Parsing → Section Extraction → 
Metadata Enrichment → Cache → Return
```

**Parsing des sections 10-K :**
- **Item 1** : Business Description
- **Item 1A** : Risk Factors
- **Item 2** : Properties
- **Item 3** : Legal Proceedings
- **Item 7** : MD&A (Management Discussion & Analysis)
- **Item 7A** : Quantitative & Qualitative Disclosures
- **Item 8** : Financial Statements

**Technique de parsing :**
- Regex patterns pour identifier les sections
- Nettoyage HTML (suppression scripts, styles)
- Limitation de taille : 5000 chars par section (optimisation mémoire)

### 3.3. Pipeline RAG - Ingestion

```python
class DocumentIngester:
    def ingest_documents(self, documents: List[Document]) -> VectorStoreIndex:
        # 1. Text Splitting
        # 2. Embedding Generation
        # 3. Vector Storage
```

**Processus de chunking :**
- **Chunk Size** : 1024 tokens (équilibre contexte/précision)
- **Overlap** : 200 tokens (évite perte d'information aux frontières)
- **Splitter** : `SentenceSplitter` (découpe par phrases complètes)
- **Métadonnées** : ticker, year, section, document_type

**Stockage vectoriel :**
- **Format** : Vecteurs 384D (BGE embeddings)
- **Index** : HNSW pour recherche rapide O(log n)
- **Collections** : Une par ticker pour isolation
- **Persistance** : ChromaDB sauvegarde sur disque

---

## 4. Architecture Logicielle

### 4.1. Structure Modulaire

```
src/
├── agents/
│   ├── finance_agent.py    # Agent ReAct principal
│   └── tools.py            # Définition des outils
├── data/
│   ├── alpha_vantage.py    # Client API marché
│   └── sec_edgar.py        # Client API SEC + parsing
├── rag/
│   ├── ingestion.py        # Indexation documents
│   └── retrieval.py        # Recherche vectorielle
└── ui/
    └── dashboard.py        # Interface Streamlit
```

### 4.2. Séparation des Responsabilités

| Module | Responsabilité | Dépendances |
|--------|---------------|-------------|
| `finance_agent.py` | Orchestration agent, pattern ReAct | tools, rag, llm |
| `tools.py` | Définition outils agent | alpha_vantage, rag |
| `alpha_vantage.py` | Accès données marché, cache, rate limiting | requests, pandas |
| `sec_edgar.py` | Téléchargement et parsing 10-K | sec-edgar-downloader, beautifulsoup4 |
| `ingestion.py` | Chunking, embeddings, indexation | llama-index, chromadb |
| `retrieval.py` | Recherche vectorielle, filtrage | llama-index |
| `dashboard.py` | UI, orchestration, état session | streamlit, tous modules |

### 4.3. Gestion d'État

**Streamlit Session State :**
```python
st.session_state['rag_retriever'] = retriever
st.session_state['report_data'] = report_data
st.session_state['current_ticker'] = ticker
st.session_state['agent'] = agent
st.session_state['messages'] = []  # Historique chat
```

**Cache Streamlit :**
- `@st.cache_resource` : Pour clients API (réutilisés entre re-runs)
- `@st.cache_data` : Pour données calculées (non utilisé, préférence cache manuel)

---

## 5. Détails d'Implémentation du Code

### 5.1. Pattern ReAct Agent

```python
class FinanceAgent:
    def __init__(self, rag_retriever, alpha_vantage_client, llm):
        tools = get_all_tools(rag_retriever, alpha_vantage_client, llm)
        
        self.agent = ReActAgent.from_tools(
            tools=tools,
            llm=llm,
            verbose=verbose,
            system_prompt=self.SYSTEM_PROMPT,
            max_iterations=10  # Limite pour éviter boucles infinies
        )
```

**Cycle ReAct (Reason + Act) :**

```
1. Thought: "L'utilisateur demande les risques. Je dois chercher dans le rapport 10-K."
2. Action: analyze_10k_report(question="risques", section="Item 1A")
3. Observation: "Les risques incluent: changement climatique, réglementation..."
4. Thought: "L'utilisateur veut aussi savoir le prix actuel de l'action."
5. Action: get_stock_metrics(symbol="AAPL")
6. Observation: "Prix: $150.00, PE: 28.5..."
7. Thought: "J'ai toutes les informations. Je peux maintenant répondre."
8. Final Answer: "Voici les principaux risques et la situation boursière..."
```

**Limites de sécurité :**
- `max_iterations=10` : Évite les boucles infinies
- Timeout implicite via API limits
- Gestion d'erreurs dans chaque outil

### 5.2. Outils (Tools) de l'Agent

#### Outil 1 : Analyse Rapport 10-K

```python
def analyze_10k_report(question: str, section: Optional[str] = None) -> str:
    metadata_filters = {'section': section} if section else None
    response = rag_retriever.query(query=question, metadata_filters=metadata_filters)
    return response
```

**Fonctionnalités :**
- Recherche sémantique dans le rapport
- Filtrage optionnel par section (Item 1A, Item 7, etc.)
- Synthèse automatique via LLM
- Citation des sources (via métadonnées)

#### Outil 2 : Métriques Boursières

```python
def get_stock_metrics(symbol: str) -> str:
    quote = alpha_vantage_client.get_quote(symbol)
    overview = alpha_vantage_client.get_company_overview(symbol)
    # Formatage structuré pour l'agent
    return formatted_metrics
```

**Données récupérées :**
- Prix actuel, variations
- Métriques fondamentales (PE, EPS, dividend yield)
- Informations entreprise (secteur, industrie)
- Statistiques 52 semaines

#### Outil 3 : Séries Temporelles

```python
def get_stock_time_series(symbol: str, days: int = 30) -> str:
    df = alpha_vantage_client.get_time_series_daily(symbol)
    sma_20 = calculate_sma(df, window=20)
    rsi = calculate_rsi(df, window=14)
    # Calculs indicateurs techniques
    return summary
```

**Indicateurs calculés :**
- **SMA 20** : Moving Average 20 jours (tendance)
- **RSI 14** : Relative Strength Index (survente/surachat)
- Variations prix, volumes moyens

### 5.3. Recherche Vectorielle Avancée

```python
class AdvancedRAGRetriever:
    def __init__(self, index, llm, similarity_top_k=5, rerank_top_k=3):
        self.retriever = VectorIndexRetriever(index, similarity_top_k=5)
        self.postprocessor = SimilarityPostprocessor(similarity_cutoff=0.7)
```

**Pipeline de récupération :**

```
Query → Embedding (BGE) → Vector Search (ChromaDB) → 
Top-K Chunks (k=5) → Similarity Filter (>0.7) → 
Context Assembly → LLM Synthesis → Response
```

**Optimisations :**
- Filtrage par métadonnées (section, ticker, year)
- Post-processing pour éliminer résultats non pertinents
- Limitation du contexte (top-K) pour réduire coûts LLM

### 5.4. Rate Limiting et Cache

#### Décorateur Rate Limiting

```python
def rate_limited(max_per_minute: int = 5):
    min_interval = 60.0 / max_per_minute
    last_called = [0.0]  # Closure pour persistance
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator
```

**Fonctionnement :**
- Token Bucket simplifié
- Partage d'état via closure
- Sleep automatique si limite atteinte

#### Système de Cache

```python
def _get_cache_path(self, symbol: str, function: str) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    return f"data/raw/{symbol}_{function}_{today}.json"
```

**Stratégie :**
- Cache quotidien (invalidation naturelle)
- Fichiers JSON lisibles (debugging facile)
- Check avant chaque appel API
- Sauvegarde après réception réponse

---

## 6. Patterns de Design

### 6.1. Singleton Pattern (Clients API)

```python
@st.cache_resource
def initialize_clients():
    # Création unique, réutilisée entre re-runs Streamlit
    alpha_client = AlphaVantageClient()
    sec_client = SecEdgarClient()
    return alpha_client, sec_client
```

**Avantages :**
- Évite réinitialisations inutiles
- Partage d'état (cache, rate limiting)
- Performance améliorée

### 6.2. Factory Pattern (Tools)

```python
def create_financial_report_tool(rag_retriever, llm) -> FunctionTool:
    def analyze_10k_report(question: str, section: Optional[str] = None):
        # Implementation
    return FunctionTool.from_defaults(fn=analyze_10k_report, ...)
```

**Avantages :**
- Encapsulation de la création d'outils
- Configuration flexible
- Réutilisabilité

### 6.3. Strategy Pattern (Response Modes)

```python
def query(self, query: str, response_mode: ResponseMode = ResponseMode.COMPACT):
    # Mode COMPACT: Synthèse concise
    # Mode TREE_SUMMARIZE: Arbre de synthèse
    # Mode REFINE: Raffinement itératif
```

**Modes disponibles :**
- `COMPACT` : Par défaut, rapide
- `TREE_SUMMARIZE` : Pour documents longs
- `REFINE` : Pour précision maximale

### 6.4. Decorator Pattern (Rate Limiting)

Voir section 5.4 pour détails d'implémentation.

---

## 7. Flux de Données et Processus

### 7.1. Flux Complet - Analyse d'une Entreprise

```
┌─────────────────────────────────────────────────────────────┐
│                    UTILISATEUR                               │
│  Entrée: Ticker "AAPL" + Clic "Lancer l'Analyse"           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              DASHBOARD.PY - ORCHESTRATION                   │
│  1. Vérification clés API                                   │
│  2. Initialisation clients (cached)                         │
│  3. Initialisation LLM (cached)                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
        ▼                                     ▼
┌──────────────────┐              ┌──────────────────────┐
│ ALPHA VANTAGE    │              │   SEC EDGAR CLIENT   │
│   CLIENT         │              │                      │
│                  │              │                      │
│ 1. Check cache   │              │ 1. Ticker → CIK      │
│ 2. API call      │              │ 2. Download 10-K     │
│ 3. Parse JSON    │              │ 3. Parse HTML        │
│ 4. Cache save    │              │ 4. Extract sections  │
│ 5. Return data   │              │ 5. Cache save        │
└──────────────────┘              └──────────┬───────────┘
        │                                     │
        │                                     ▼
        │                          ┌──────────────────────┐
        │                          │  DOCUMENT INGESTER   │
        │                          │                      │
        │                          │ 1. Create Documents  │
        │                          │ 2. Text Splitting    │
        │                          │ 3. Generate Embed.   │
        │                          │ 4. Index in ChromaDB │
        │                          └──────────┬───────────┘
        │                                     │
        └─────────────────┬───────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT UI                             │
│                                                             │
│  Tab 1: Dashboard Marché                                    │
│    - Graphique Plotly (prix, SMA, RSI, volume)             │
│    - Métriques KPIs (PE, market cap, etc.)                 │
│                                                             │
│  Tab 2: Assistant Financier                                 │
│    - Chat interface                                         │
│    - Agent ReAct prêt (RAG + Market tools)                 │
│                                                             │
│  Tab 3: Explorateur Documents                               │
│    - Sections 10-K                                          │
│    - Métadonnées                                            │
└─────────────────────────────────────────────────────────────┘
```

### 7.2. Flux - Question à l'Assistant

```
User Question: "Quels sont les risques et le prix actuel?"
        │
        ▼
┌──────────────────────────────────────┐
│      FINANCE AGENT (ReAct)           │
│                                      │
│  Thought 1: "Besoin risques 10-K"   │
│  Action 1: analyze_10k_report(...)  │
│    │                                  │
│    ├─> AdvancedRAGRetriever         │
│    │     │                            │
│    │     ├─> Query → Embedding       │
│    │     ├─> Vector Search (ChromaDB)│
│    │     ├─> Top-K Chunks            │
│    │     └─> LLM Synthesis           │
│    │                                  │
│    └─> Observation: "Risques: ..."   │
│                                      │
│  Thought 2: "Besoin prix actuel"    │
│  Action 2: get_stock_metrics(...)   │
│    │                                  │
│    ├─> AlphaVantageClient           │
│    │     │                            │
│    │     ├─> Check Cache             │
│    │     ├─> API Call (if needed)    │
│    │     └─> Return Metrics          │
│    │                                  │
│    └─> Observation: "Prix: $150..."  │
│                                      │
│  Thought 3: "J'ai tout, je réponds" │
│  Final Answer: "Les risques sont... │
│                et le prix actuel..."│
└──────────────────────────────────────┘
        │
        ▼
   User sees response
```

---

## 8. Optimisations et Performance

### 8.1. Optimisations Mémoire

**Chunking Intelligent :**
- Limite de 5000 caractères par section (évite overflow)
- Chunks de 1024 tokens (équilibre contexte/précision)
- Overlap de 200 tokens (préserve contexte)

**Gestion Collections ChromaDB :**
- Une collection par ticker (isolation, cleanup facile)
- Nettoyage automatique anciennes collections
- Persistence sur disque (pas de RAM excessive)

### 8.2. Optimisations Latence

**Cache Multi-Niveau :**
1. **Streamlit cache** : Clients API réutilisés
2. **Fichier cache** : Données API quotidiennes
3. **ChromaDB cache** : Index vectoriel persistant

**Parallélisation :**
- Téléchargement SEC et appel Alpha Vantage peuvent être parallélisés (futur)
- Recherche vectorielle optimisée par HNSW (O(log n))

**Rate Limiting Intelligent :**
- Prévention des appels inutiles
- Sleep automatique si limite atteinte
- Priorité aux données critiques

### 8.3. Optimisations Coût

**Embeddings Locaux :**
- Pas de coût API pour embeddings
- Modèle BGE petit (~500MB)
- Exécution CPU acceptable

**Cache Agressif :**
- Réduit appels API répétés
- Données marché: cache quotidien
- Données SEC: cache permanent (rapports ne changent pas)

**LLM Efficace :**
- Temperature 0 (pas de génération multiple)
- Mode COMPACT pour synthèse courte
- Limite de contexte (top-K chunks)

---

## 9. Gestion des Erreurs et Résilience

### 9.1. Stratégies de Gestion d'Erreurs

#### Erreurs API Alpha Vantage

```python
try:
    response = requests.get(url, timeout=10)
    if "Error Message" in data:
        raise ValueError(f"API Error: {data['Error Message']}")
    if "Note" in data:
        raise ValueError(f"Rate Limit: {data['Note']}")
except requests.exceptions.RequestException as e:
    raise ConnectionError(f"Failed to connect: {e}")
```

**Gestion :**
- Timeout 10s (évite blocage)
- Vérification erreurs API explicites
- Messages d'erreur clairs pour utilisateur

#### Erreurs SEC EDGAR

```python
try:
    cik = self.get_ticker_to_cik(ticker)
    if not cik:
        raise ValueError(f"CIK not found for {ticker}")
    html_path = self.download_10k(ticker)
except Exception as e:
    raise RuntimeError(f"Failed to download 10-K: {e}")
```

**Gestion :**
- Vérification CIK avant téléchargement
- Gestion fichiers manquants
- Fallback sur cache si disponible

#### Erreurs LLM

```python
try:
    llm = Gemini(model=model_name, ...)
except Exception as e:
    if "404" in str(e) or "not found" in str(e).lower():
        # Fallback sur modèle alternatif
        llm = Gemini(model="models/gemini-1.5-flash", ...)
    else:
        raise e
```

**Gestion :**
- Détection erreurs modèle (404)
- Fallback automatique modèle alternatif
- Messages d'erreur utilisateur-friendly

### 9.2. Résilience du Système

**Graceful Degradation :**
- Si Alpha Vantage échoue → Afficher message, continuer avec SEC
- Si SEC échoue → Utiliser cache si disponible
- Si LLM échoue → Message d'erreur clair, pas de crash

**Validation des Entrées :**
- Vérification format ticker (uppercase, validation)
- Vérification clés API (format, présence)
- Sanitization des queries utilisateur

---

## 10. Sécurité et Bonnes Pratiques

### 10.1. Gestion des Secrets

**Variables d'Environnement :**
```python
api_key = os.getenv("GEMINI_API_KEY")
# Jamais hardcodé dans le code
```

**Fichier .env :**
- Ajouté à `.gitignore`
- Template fourni (`env.template`)
- Pas de secrets dans le repository

**Streamlit Secrets :**
- Support pour Streamlit Cloud
- Interface sécurisée pour saisie clés

### 10.2. Validation et Sanitization

**Input Validation :**
- Ticker : Conversion uppercase, validation format
- Queries : Pas de sanitization excessive (preserve sens)
- API Keys : Vérification format basique

**Output Sanitization :**
- Échappement HTML dans Streamlit (automatique)
- Pas d'exécution de code utilisateur
- Limitation taille réponses LLM

### 10.3. Bonnes Pratiques Code

**Type Hints :**
```python
def get_quote(self, symbol: str) -> Dict:
    # Types explicites pour documentation et vérification
```

**Docstrings :**
- Documentation complète de chaque fonction
- Args et Returns documentés
- Exemples d'utilisation

**Error Handling :**
- Try/except spécifiques (pas de catch-all)
- Messages d'erreur informatifs
- Logging des erreurs (à améliorer)

---

## 11. Métriques et Monitoring

### 11.1. Métriques de Performance

**Temps de Réponse Typiques :**
- Initialisation clients : ~100ms (cached)
- Téléchargement 10-K : ~5-30s (selon réseau)
- Indexation documents : ~10-60s (selon taille)
- Recherche vectorielle : ~50-200ms
- Synthèse LLM : ~500-2000ms

**Utilisation Ressources :**
- RAM : ~500MB-1GB (selon taille documents)
- Disque : ~10MB par ticker (cache + vector DB)
- CPU : Modéré (embeddings), faible (recherche)

### 11.2. Métriques Qualité RAG

**Métriques RAGAS (non implémentées mais prévues) :**
- **Faithfulness** : Réponse basée sur contexte source
- **Context Recall** : Information nécessaire trouvée
- **Answer Relevance** : Pertinence réponse à la question

**Métriques Métier :**
- Précision citations (sections correctes)
- Cohérence temporelle (pas de mélange années)
- Complétude information (tous risques mentionnés)

---

## 12. Extensions Futures

### 12.1. Améliorations Techniques

**RAG Avancé :**
- Reranking avec modèle cross-encoder
- Hybrid search (vectoriel + BM25)
- Query expansion automatique

**Agent Amélioré :**
- Mémoire conversationnelle persistante
- Planification multi-étapes
- Auto-correction et réflexion

**Performance :**
- Parallélisation téléchargements
- Optimisation requêtes ChromaDB
- Mise en cache embeddings

### 12.2. Nouvelles Fonctionnalités

**Sources Données :**
- Transcripts d'appels investisseurs
- News sentiment analysis
- Options chain data

**Analyses :**
- Comparaison multi-entreprises
- Prédiction tendances (time series)
- Détection anomalies

**Interface :**
- Export PDF rapports
- Graphiques avancés (candlesticks, etc.)
- Dashboard personnalisable

---

## Conclusion

Cette documentation technique couvre tous les aspects du projet FinSight AI :
- **Architecture** : Design modulaire, séparation des responsabilités
- **Modèles IA** : LLM, embeddings, vector DB configurés optimalement
- **Code** : Patterns de design, optimisations, gestion erreurs
- **Données** : Pipelines ETL robustes, cache intelligent
- **Performance** : Optimisations mémoire, latence, coût

Le système est conçu pour être :
- ✅ **Robuste** : Gestion erreurs complète
- ✅ **Efficace** : Cache multi-niveaux, rate limiting
- ✅ **Maintenable** : Code modulaire, documentation complète
- ✅ **Extensible** : Architecture permet ajouts faciles

---

**Document généré le** : Décembre 2024  
**Version** : 1.0  
**Auteur** : Documentation automatique

