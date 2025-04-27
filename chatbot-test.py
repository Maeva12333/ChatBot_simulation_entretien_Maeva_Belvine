import os
import streamlit as st
import PyPDF2
import docx
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

# Config Streamlit
st.set_page_config(page_title="Chatbot Entretien RH", layout="wide")
st.title("🤖 Chatbot d'entretien RH ")

# Config modèle LLM
os.environ["GROQ_API_KEY"] = "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"
llm = init_chat_model("llama3-70b-8192", model_provider="groq", temperature=0.7)


# --- Fonctions Utilitaires ---

def lire_fichier(uploaded_file):
    """
    Extrait le texte d'un fichier téléchargé, selon son format.

    Parameters
    ----------
    uploaded_file : UploadedFile
        Le fichier téléchargé par l'utilisateur, qui peut être au format PDF, DOCX ou TXT.

    Returns
    -------
    str
        Le contenu extrait du fichier sous forme de chaîne de caractères.
        Si le format est non supporté, retourne une message indiquant l'erreur.
    """
    if uploaded_file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        return "".join([page.extract_text() for page in reader.pages])
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])
    elif uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")
    else:
        return "[Format non supporté]"


def generer_reponse(messages):
    """
    Génère une réponse du modèle de langage en fonction des messages passés.

    Parameters
    ----------
    messages : list of HumanMessage
        Liste des messages échangés pendant l'entretien, dont la dernière entrée est la question en cours.

    Returns
    -------
    HumanMessage
        Réponse générée par le modèle de langage.
    """
    return llm.invoke(messages)


def feedback(cv_content, fiche_poste_content, messages):
    """
    Génère un retour sur la pertinence du CV et sur la qualité des réponses pendant l'entretien.

    Parameters
    ----------
    cv_content : str
        Le contenu du CV sous forme de texte.
    fiche_poste_content : str
        Le contenu de la fiche de poste sous forme de texte.
    messages : list of HumanMessage
        Historique des messages échangés pendant l'entretien.

    Returns
    -------
    tuple of str
        - Retour sur la pertinence du CV par rapport à la fiche de poste.
        - Retour sur la qualité des réponses de l'entretien (clarté, pertinence, etc.).
    """
    cv_prompt = f"""Voici le contenu du CV :
{cv_content}

Voici la fiche de poste :
{fiche_poste_content}

Évalue la pertinence du CV par rapport à la fiche de poste, avec des points forts et des axes d'amélioration."""

    entretien_prompt = f"""Voici l'historique de l'entretien :
{chr(10).join([msg.content for msg in messages[1:]])}

Donne un retour constructif sur les réponses du candidat : clarté, pertinence, structure, et capacité d'argumentation."""

    cv_feedback = generer_reponse([HumanMessage(content=cv_prompt)])
    entretien_feedback = generer_reponse([HumanMessage(content=entretien_prompt)])

    return cv_feedback.content, entretien_feedback.content


# --- Interface Utilisateur ---

with st.sidebar:
    st.header("📁 Chargement des fichiers")
    cv_file = st.file_uploader("CV (pdf, docx, txt)", type=["pdf", "docx", "txt"])
    fiche_poste_file = st.file_uploader("Fiche de poste", type=["pdf", "docx", "txt"])

    st.header("🌐 Paramètres")
    langue = st.selectbox("Langue de l'entretien", ["Français", "Anglais", "Espagnol", "Allemand"])

    if st.button("🟢 Démarrer l'entretien") and cv_file and fiche_poste_file:
        """
        Démarre l'entretien en fonction des fichiers et paramètres sélectionnés.

        Récupère le contenu des fichiers téléchargés et initialise les messages d'entretien. 
        En fonction de la langue choisie, prépare un prompt pour interroger le modèle.
        """
        st.session_state['start'] = True
        st.session_state['cv_content'] = lire_fichier(cv_file)
        st.session_state['fiche_poste_content'] = lire_fichier(fiche_poste_file)
        st.session_state['messages'] = []

        # Définir le contexte en fonction de la langue choisie
        if langue == "Français":
            context = f"""
            Tu es un recruteur RH en train de faire passer un entretien d'embauche.
            Voici le contenu du CV du candidat :
            {st.session_state['cv_content']}

            Voici la fiche de poste pour laquelle il postule :
            {st.session_state['fiche_poste_content']}

            Pose des questions pertinentes, une par une, comme dans un entretien réel. 
            Attends à chaque fois la réponse de l'utilisateur avant de continuer.
            """
            premiere_question = "Pouvez-vous vous présenter ?"
        elif langue == "Anglais":
            context = f"""
            You are an HR recruiter doing a job interview.
            Here's the candidate's CV:
            {st.session_state['cv_content']}

            Here's the job description they're applying for:
            {st.session_state['fiche_poste_content']}

            Ask relevant questions, one at a time, like in a real interview.
            Wait for the user's response before continuing.
            """
            premiere_question = "Can you introduce yourself?"
        elif langue == "Espagnol":
            context = f"""
            Eres un reclutador de RRHH haciendo una entrevista de trabajo.
            Aquí está el CV del candidato:
            {st.session_state['cv_content']}

            Aquí la descripción del puesto al que está aplicando:
            {st.session_state['fiche_poste_content']}

            Haz preguntas relevantes, una a la vez, como en una entrevista real.
            Espera la respuesta del usuario antes de continuar.
            """
            premiere_question = "¿Puede presentarse?"
        else:
            context = f"""
            Du bist ein HR-Recruiter im Vorstellungsgespräch.
            Hier ist der Lebenslauf des Kandidaten:
            {st.session_state['cv_content']}

            Hier die Stellenbeschreibung, für die der Kandidat sich bewirbt:
            {st.session_state['fiche_poste_content']}

            Stelle relevante Fragen, eine nach der anderen, wie in einem echten Vorstellungsgespräch.
            Warte auf die Antwort des Benutzers, bevor du fortfährst.
            """
            premiere_question = "Können Sie sich bitte vorstellen?"

        # Initialiser les messages
        st.session_state['messages'].append(HumanMessage(content=context))

        # Ajouter la première question du recruteur
        st.session_state['messages'].append(HumanMessage(content=premiere_question))
        st.session_state['chat_history'] = [("recruteur", premiere_question)]

# --- Partie principale : entretien ---

if st.session_state.get('start', False):

    st.subheader("🗨️ Entretien en cours")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for sender, msg in st.session_state.chat_history:
        with st.chat_message(sender):
            st.markdown(msg)

    if user_input := st.chat_input("Votre réponse ici..."):
        st.session_state['messages'].append(HumanMessage(content=user_input))
        st.session_state.chat_history.append(("user", user_input))

        response = generer_reponse(st.session_state['messages'])
        st.session_state['messages'].append(HumanMessage(content=response.content))
        st.session_state.chat_history.append(("assistant", response.content))

        with st.chat_message("assistant"):
            st.markdown(response.content)

    # Afficher feedback à la fin
    if st.button("🛑 Terminer l'entretien et obtenir le feedback"):
        with st.spinner("Analyse du CV et de l'entretien..."):
            cv_fb, entretien_fb = feedback(
                st.session_state['cv_content'],
                st.session_state['fiche_poste_content'],
                st.session_state['messages']
            )
        st.success("✅ Feedback généré avec succès !")

        st.subheader("📄 Feedback sur le CV")
        st.markdown(cv_fb)

        st.subheader("🗣️ Feedback sur l'entretien")
        st.markdown(entretien_fb)
