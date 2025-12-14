"""
Reusable UI components for FinSight AI
"""
import streamlit as st
from typing import Optional


def show_welcome_screen():
    """Display welcome screen - Analytics Dashboard Style"""
    st.markdown("""
    <div style='background: #FFFFFF; border: 1px solid #E2E8F0; 
                padding: 2.5rem; border-radius: 12px; text-align: center; 
                margin-bottom: 2rem; box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05);'>
        <h1 style='font-family: Inter, sans-serif; color: #1A202C; font-size: 2rem; 
                   margin-bottom: 0.75rem; font-weight: 700;'>
            Bienvenue sur FinSight AI
        </h1>
        <p style='font-family: Inter, sans-serif; font-size: 1rem; color: #718096; margin: 0;'>
            Votre plateforme d'analyse financière intelligente
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem; background: #FFFFFF; 
                    border: 1px solid #E2E8F0; border-radius: 12px; margin: 0.5rem;
                    box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05);'>
            <h3 style='font-family: Inter, sans-serif; color: #1A202C; font-size: 1rem; 
                       font-weight: 600; margin-bottom: 0.5rem;'>Dashboard</h3>
            <p style='font-family: Inter, sans-serif; color: #718096; font-size: 0.875rem; 
                     margin: 0;'>Visualisez les données de marché en temps réel</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem; background: #FFFFFF; 
                    border: 1px solid #E2E8F0; border-radius: 12px; margin: 0.5rem;
                    box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05);'>
            <h3 style='font-family: Inter, sans-serif; color: #1A202C; font-size: 1rem; 
                       font-weight: 600; margin-bottom: 0.5rem;'>Assistant IA</h3>
            <p style='font-family: Inter, sans-serif; color: #718096; font-size: 0.875rem; 
                     margin: 0;'>Posez des questions sur les rapports financiers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem; background: #FFFFFF; 
                    border: 1px solid #E2E8F0; border-radius: 12px; margin: 0.5rem;
                    box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05);'>
            <h3 style='font-family: Inter, sans-serif; color: #1A202C; font-size: 1rem; 
                       font-weight: 600; margin-bottom: 0.5rem;'>Documents</h3>
            <p style='font-family: Inter, sans-serif; color: #718096; font-size: 0.875rem; 
                     margin: 0;'>Explorez les rapports SEC 10-K</p>
        </div>
        """, unsafe_allow_html=True)


def show_quick_start_guide():
    """Display quick start guide"""
    with st.expander("📖 Guide de Démarrage Rapide", expanded=False):
        st.markdown("""
        ### 🎯 Étapes pour commencer :
        
        1. **Configurez vos clés API** (dans la sidebar à gauche)
           - 🔑 **Gemini API** : [Obtenir gratuitement](https://aistudio.google.com/app/apikey)
           - 🔑 **Alpha Vantage API** : [Obtenir gratuitement](https://www.alphavantage.co/support/#api-key)
        
        2. **Entrez un symbole boursier** (ex: AAPL, MSFT, GOOGL)
        
        3. **Cliquez sur "Lancer l'Analyse"**
        
        4. **Explorez les résultats** dans les différents onglets
        
        ### 💡 Exemples de questions pour l'Assistant :
        - "Quels sont les principaux risques identifiés dans le rapport ?"
        - "Quelle est la stratégie de croissance de l'entreprise ?"
        - "Compare le sentiment du rapport avec la performance boursière récente"
        - "L'action est-elle surévaluée par rapport aux risques mentionnés ?"
        
        ### ⚠️ Besoin d'aide ?
        Consultez la documentation complète ou contactez le support.
        """)


def show_api_key_help():
    """Display help for API keys"""
    with st.expander("❓ Comment obtenir les clés API ?", expanded=False):
        st.markdown("""
        ### 🔑 Clé API Gemini (Google)
        
        1. Allez sur [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Connectez-vous avec votre compte Google
        3. Cliquez sur "Create API Key"
        4. Copiez la clé (commence par `AIza...`)
        5. Collez-la dans le champ "Gemini API Key"
        
        ✅ **Gratuit** : 60 requêtes/min, 1500 requêtes/jour
        
        ---
        
        ### 🔑 Clé API Alpha Vantage
        
        1. Allez sur [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
        2. Remplissez le formulaire (nom, email)
        3. Vérifiez votre email
        4. Copiez la clé API reçue
        5. Collez-la dans le champ "Alpha Vantage API Key"
        
        ✅ **Gratuit** : 5 requêtes/min, 500 requêtes/jour
        """)


def show_example_questions():
    """Display example questions for the assistant"""
    st.markdown("### 💡 Exemples de Questions")
    
    example_questions = [
        "Quels sont les principaux risques identifiés dans le rapport ?",
        "Quelle est la stratégie de croissance de l'entreprise ?",
        "Compare le sentiment du rapport avec la performance boursière récente",
        "L'action est-elle surévaluée par rapport aux risques mentionnés ?",
        "Quels sont les facteurs de risque liés au changement climatique ?",
        "Quelle est la position concurrentielle de l'entreprise ?",
        "Analyse la rentabilité et les marges de l'entreprise",
        "Quels sont les défis futurs mentionnés dans le rapport ?"
    ]
    
    cols = st.columns(2)
    for i, question in enumerate(example_questions):
        with cols[i % 2]:
            if st.button(f"💬 {question}", key=f"example_{i}", use_container_width=True):
                return question
    return None


def show_error_with_solution(error_message: str, solution: str):
    """Display error with helpful solution"""
    st.error(f"""
    **❌ Erreur :** {error_message}
    
    **💡 Solution :** {solution}
    """)


def show_success_message(message: str):
    """Display success message"""
    st.success(f"✅ {message}")


def show_info_card(title: str, content: str, icon: str = "ℹ️"):
    """Display an info card - Analytics Dashboard Style"""
    st.markdown(f"""
    <div style='background: #EBF8FF; border: 1px solid #BEE3F8; 
                padding: 1.25rem; border-radius: 8px; 
                border-left: 4px solid #3182CE; margin: 1rem 0;'>
        <h4 style='font-family: Inter, sans-serif; color: #2C5282; margin-bottom: 0.5rem; 
                   font-size: 0.875rem; font-weight: 600;'>
            {icon} {title}
        </h4>
        <p style='font-family: Inter, sans-serif; color: #2C5282; margin: 0; 
                  font-size: 0.875rem;'>{content}</p>
    </div>
    """, unsafe_allow_html=True)

