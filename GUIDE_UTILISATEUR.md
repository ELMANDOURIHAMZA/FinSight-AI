# 📖 Guide Utilisateur - FinSight AI

> **Guide complet pour utiliser FinSight AI de manière efficace**

---

## 🎯 Table des Matières

1. [Première Utilisation](#première-utilisation)
2. [Configuration](#configuration)
3. [Utilisation du Dashboard](#utilisation-du-dashboard)
4. [Utilisation de l'Assistant IA](#utilisation-de-lassistant-ia)
5. [Exploration des Documents](#exploration-des-documents)
6. [Conseils et Astuces](#conseils-et-astuces)
7. [Résolution de Problèmes](#résolution-de-problèmes)

---

## 🚀 Première Utilisation

### Étape 1 : Accéder à l'Application

1. Ouvrez votre navigateur web (Chrome, Firefox, Safari, Edge)
2. Accédez à l'URL de l'application (fournie par votre administrateur)
3. Vous verrez l'écran de bienvenue

### Étape 2 : Configuration Initiale

**Avant de commencer, vous devez configurer vos clés API :**

#### 🔑 Obtenir la Clé API Gemini (Google)

1. Allez sur [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Connectez-vous avec votre compte Google
3. Cliquez sur **"Create API Key"**
4. **Copiez immédiatement** la clé (elle commence par `AIza...`)
5. Collez-la dans le champ **"Gemini API Key"** dans la sidebar

> ✅ **Gratuit** : 60 requêtes/minute, 1500 requêtes/jour

#### 🔑 Obtenir la Clé API Alpha Vantage

1. Allez sur [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Remplissez le formulaire (nom, email)
3. Vérifiez votre boîte email
4. **Copiez la clé API** reçue par email
5. Collez-la dans le champ **"Alpha Vantage API Key"** dans la sidebar

> ✅ **Gratuit** : 5 requêtes/minute, 500 requêtes/jour

### Étape 3 : Première Analyse

1. Une fois les clés configurées, entrez un **symbole boursier** (ex: `AAPL` pour Apple)
2. Cliquez sur **"🚀 Lancer l'Analyse"**
3. Attendez le chargement (30-60 secondes pour la première fois)
4. Explorez les résultats dans les différents onglets

---

## ⚙️ Configuration

### Sidebar - Paramètres

La sidebar gauche contient tous les paramètres :

#### 🔑 Clés API
- **Gemini API Key** : Clé pour l'intelligence artificielle
- **Alpha Vantage API Key** : Clé pour les données de marché

> 💡 **Astuce** : Les clés sont sauvegardées pour votre session. Vous n'avez pas besoin de les ré-entrer à chaque fois.

#### 🤖 Modèle IA
- **gemini-2.0-flash-exp** : Rapide et efficace (recommandé)
- **gemini-1.5-pro** : Plus précis mais plus lent
- **gemini-1.5-flash** : Équilibre vitesse/précision

#### 📈 Symbole Boursier
- Entrez le symbole de l'entreprise (ex: `AAPL`, `MSFT`, `GOOGL`)
- Utilisez les boutons rapides pour les entreprises populaires
- Le symbole est automatiquement converti en majuscules

---

## 📊 Utilisation du Dashboard

### Onglet "Dashboard Marché"

Cet onglet affiche :

#### 📊 Métriques Clés
- **💰 Prix Actuel** : Prix de l'action avec variation
- **🏢 Capitalisation** : Valeur totale de l'entreprise
- **📈 Ratio P/E** : Price-to-Earnings ratio
- **💵 Rendement Dividende** : Pourcentage de dividende

#### 📈 Graphique Technique
- **Prix et Moyennes Mobiles** : Prix de clôture, SMA 20, SMA 50
- **Volume** : Volume d'échanges (vert = hausse, rouge = baisse)
- **RSI** : Relative Strength Index (indicateur de survente/surachat)

> 💡 **Astuce** : Survolez les graphiques pour voir les valeurs détaillées

#### 🏢 Informations Entreprise
- Nom, secteur, industrie
- 52 semaines High/Low
- Beta (volatilité relative au marché)
- Description de l'entreprise

---

## 💬 Utilisation de l'Assistant IA

### Comment Poser des Questions

L'assistant IA comprend le langage naturel. Posez vos questions comme vous parleriez à un analyste financier.

#### ✅ Exemples de Questions Efficaces

**Questions sur les Risques :**
- "Quels sont les principaux risques identifiés dans le rapport ?"
- "Quels sont les risques liés au changement climatique ?"
- "Quels sont les risques réglementaires mentionnés ?"

**Questions sur la Stratégie :**
- "Quelle est la stratégie de croissance de l'entreprise ?"
- "Quels sont les plans d'expansion mentionnés ?"
- "Comment l'entreprise se positionne-t-elle face à la concurrence ?"

**Questions Analytiques :**
- "Compare la performance boursière avec les risques mentionnés"
- "L'action est-elle surévaluée par rapport aux risques ?"
- "Quelle est la position concurrentielle de l'entreprise ?"

**Questions sur les Performances :**
- "Analyse la rentabilité et les marges de l'entreprise"
- "Quels sont les facteurs qui affectent les revenus ?"
- "Comment l'entreprise gère-t-elle ses coûts ?"

### Fonctionnalités de l'Assistant

- ✅ **Réponses avec Citations** : L'assistant cite les sections du rapport
- ✅ **Analyse Combinée** : Combine données de marché et rapport 10-K
- ✅ **Contexte Complet** : Utilise tout le rapport pour répondre
- ✅ **Langage Naturel** : Comprend les questions en français

### Boutons Utiles

- **🗑️ Effacer l'historique** : Recommencez la conversation
- **💡 Voir des exemples** : Affiche des exemples de questions

---

## 📄 Exploration des Documents

### Onglet "Explorateur de Documents"

Cet onglet permet d'explorer directement le rapport 10-K :

#### Sections Disponibles

- **Item 1** : Description de l'entreprise
- **Item 1A** : Facteurs de risque
- **Item 2** : Propriétés
- **Item 3** : Procédures légales
- **Item 7** : Discussion et analyse de la direction (MD&A)
- **Item 7A** : Disclosures quantitatives et qualitatives
- **Item 8** : États financiers

#### Utilisation

1. Cliquez sur une section pour l'ouvrir
2. Lisez le contenu extrait du rapport
3. Utilisez la recherche pour trouver des informations spécifiques

---

## 💡 Conseils et Astuces

### Pour des Analyses Efficaces

1. **Soyez Spécifique** : Plus votre question est précise, meilleure sera la réponse
2. **Utilisez le Contexte** : L'assistant se souvient de votre conversation
3. **Explorez les Sections** : Utilisez l'explorateur de documents pour approfondir
4. **Combinez les Sources** : L'assistant peut combiner données de marché et rapport

### Optimisation des Performances

- **Cache** : Les données sont mises en cache pour éviter les appels API répétés
- **Limites API** : Respectez les limites (5 req/min pour Alpha Vantage)
- **Premier Chargement** : Le premier chargement peut prendre 30-60 secondes

### Meilleures Pratiques

- ✅ Vérifiez toujours vos clés API avant de commencer
- ✅ Utilisez des symboles boursiers valides (ex: AAPL, pas APPLE)
- ✅ Attendez la fin du chargement avant de poser des questions
- ✅ Reformulez votre question si la réponse n'est pas satisfaisante

---

## 🔧 Résolution de Problèmes

### Problème : "Clés API requises"

**Solution :**
1. Vérifiez que vous avez entré les deux clés dans la sidebar
2. Vérifiez le format des clés (Gemini commence par `AIza...`)
3. Vérifiez que les clés sont valides et non expirées

### Problème : "Erreur lors du chargement du rapport"

**Solutions :**
1. Vérifiez que le symbole boursier est correct
2. Assurez-vous d'avoir une connexion Internet stable
3. Réessayez dans quelques instants
4. Contactez le support si le problème persiste

### Problème : "Limite de taux API atteinte"

**Solutions :**
1. Attendez quelques minutes avant de réessayer
2. Réduisez le nombre de requêtes
3. Utilisez le cache (les données sont mises en cache quotidiennement)

### Problème : "L'assistant ne répond pas correctement"

**Solutions :**
1. Reformulez votre question de manière plus précise
2. Vérifiez que le rapport 10-K a bien été chargé
3. Utilisez des questions en français
4. Consultez les exemples de questions

### Problème : "Graphiques ne s'affichent pas"

**Solutions :**
1. Vérifiez votre connexion Internet
2. Actualisez la page (F5)
3. Vérifiez que les données de marché sont disponibles
4. Contactez le support

---

## 📞 Support

### Besoin d'Aide ?

- 📧 **Email** : support@finsight-ai.com
- 📚 **Documentation** : Consultez la documentation complète
- 💬 **Chat** : Utilisez le chat de support intégré

### Ressources

- [Guide de Démarrage Rapide](QUICKSTART.md)
- [Documentation Technique](DOCUMENTATION_TECHNIQUE.md)
- [FAQ](README.md#questions-fréquentes)

---

## ✅ Checklist de Démarrage

Avant de commencer, assurez-vous d'avoir :

- [ ] Compte Google (pour Gemini API)
- [ ] Email vérifié (pour Alpha Vantage API)
- [ ] Connexion Internet stable
- [ ] Navigateur web à jour
- [ ] Clés API configurées dans la sidebar

---

**Dernière mise à jour** : Décembre 2024  
**Version** : 1.0

