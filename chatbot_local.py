import os
import pyttsx3
import speech_recognition as sr
import PyPDF2
import docx
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

# --- Configuration de l'environnement et du modèle ---

os.environ["GROQ_API_KEY"] = "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"
engine = pyttsx3.init()  # Initialisation du moteur de synthèse vocale
llm = init_chat_model("llama3-70b-8192", model_provider="groq", temperature=0.7)  # Initialisation du modèle LLM


# --- Fonctions Utilitaires ---

def lire_fichier(fichier_path):
    """
    Extrait le contenu d'un fichier selon son format.

    Parameters
    ----------
    fichier_path : str
        Le chemin du fichier à lire. Il peut être au format PDF, DOCX ou TXT.

    Returns
    -------
    str
        Le contenu du fichier sous forme de texte. Si le format est non supporté, retourne un message d'erreur.
    """
    if fichier_path.endswith(".pdf"):
        with open(fichier_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return "".join(page.extract_text() for page in reader.pages)
    elif fichier_path.endswith(".docx"):
        doc = docx.Document(fichier_path)
        return "\n".join([p.text for p in doc.paragraphs])
    elif fichier_path.endswith(".txt"):
        with open(fichier_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "[Format non supporté]"

def parler(texte):
    """
    Fait parler le programme en convertissant le texte en parole.

    Parameters
    ----------
    texte : str
        Le texte à convertir en parole.
    """
    engine.say(texte)
    engine.runAndWait()

def ecouter_micro():
    """
    Écoute et transcrit la parole de l'utilisateur via le microphone.

    Returns
    -------
    str
        La transcription de ce qui a été dit par l'utilisateur. Retourne une chaîne vide en cas d'erreur.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Parlez maintenant...")
        audio = recognizer.listen(source)
        try:
            texte = recognizer.recognize_google(audio, language="fr-FR")
            print("Vous :", texte)
            return texte
        except sr.UnknownValueError:
            print("Désolé, je n'ai pas compris.")
            return ""
        except sr.RequestError:
            print("Erreur de service de reconnaissance vocale.")
            return ""

def generer_reponse(messages):
    """
    Génère une réponse à partir du modèle LLM en fonction des messages échangés.

    Parameters
    ----------
    messages : list of HumanMessage
        Liste des messages échangés entre l'utilisateur et le modèle.

    Returns
    -------
    HumanMessage
        La réponse générée par le modèle de langage.
    """
    return llm.invoke(messages)

def feedback(cv_content, fiche_poste_content, messages):
    """
    Fournit un feedback sur la pertinence du CV par rapport à la fiche de poste et sur les réponses durant l'entretien.

    Parameters
    ----------
    cv_content : str
        Le contenu du CV sous forme de texte.
    fiche_poste_content : str
        Le contenu de la fiche de poste sous forme de texte.
    messages : list of HumanMessage
        L'historique des messages échangés pendant l'entretien.

    Returns
    -------
    None
        Affiche directement les feedbacks sur la console.
    """
    print("\n📝 Fourniture d'un feedback sur l'entretien...")

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

    print("\n📄 Feedback sur le CV :")
    print(cv_feedback.content)

    print("\n🗣️ Feedback sur l'entretien :")
    print(entretien_feedback.content)


# --- Modes de Chatbot ---

def chatbot_textuel(messages, cv_content, fiche_poste_content):
    """
    Lance le chatbot en mode texte où l'utilisateur répond aux questions via la console.

    Parameters
    ----------
    messages : list of HumanMessage
        Historique des messages échangés.
    cv_content : str
        Le contenu du CV sous forme de texte.
    fiche_poste_content : str
        Le contenu de la fiche de poste sous forme de texte.
    """
    while True:
        response = generer_reponse(messages)
        print("\nRecruteur :", response.content)
        user_reply = input("\nVous : ")
        if user_reply.lower() in ["exit", "quit", "stop"]:
            print("\nEntretien terminé. Merci !")
            feedback(cv_content, fiche_poste_content, messages)
            break
        messages.append(HumanMessage(content=user_reply))

def chatbot_vocal(messages, cv_content, fiche_poste_content):
    """
    Lance le chatbot en mode vocal où l'utilisateur répond aux questions via la voix.

    Parameters
    ----------
    messages : list of HumanMessage
        Historique des messages échangés.
    cv_content : str
        Le contenu du CV sous forme de texte.
    fiche_poste_content : str
        Le contenu de la fiche de poste sous forme de texte.
    """
    while True:
        response = generer_reponse(messages)
        print("\nRecruteur :", response.content)
        parler(response.content)
        user_reply = ecouter_micro()
        if user_reply.lower() in ["exit", "quit", "stop"]:
            parler("Entretien terminé. Merci !")
            feedback(cv_content, fiche_poste_content, messages)
            break
        messages.append(HumanMessage(content=user_reply))


# --- Programme principal ---

if __name__ == "__main__":
    """
    Programme principal qui initialise le chatbot d'entretien avec choix de fichier et mode d'interaction.

    L'utilisateur choisit le fichier du CV, la fiche de poste et la langue de l'entretien. Ensuite, il choisit
    s'il souhaite un entretien textuel ou vocal.
    """
    cv_path = input("Veuillez entrer le chemin de votre CV (pdf, docx ou txt) : ")
    fiche_poste_path = input("Veuillez entrer le chemin de la fiche de poste : ")

    cv_content = lire_fichier(cv_path)
    fiche_poste_content = lire_fichier(fiche_poste_path)
    print("CV et fiche de poste chargés avec succès. L'entretien va commencer...\n")

    langue = input("Choisissez la langue pour l'entretien : [1] Français  [2] Anglais  [3] Espagnol  [4] Allemand\nVotre choix : ")

    if langue.strip() == "1":
        context = f"""
        Tu es un recruteur RH en train de faire passer un entretien d'embauche.
        Voici le contenu du CV du candidat :
        {cv_content}

        Voici la fiche de poste pour laquelle il postule :
        {fiche_poste_content}

        Pose des questions pertinentes, une par une, comme dans un entretien réel. 
        Attends à chaque fois la réponse de l'utilisateur avant de continuer.
        """
    elif langue.strip() == "2":
        context = f"""
        You are an HR recruiter conducting a job interview.
        Here is the content of the candidate's CV:
        {cv_content}

        Here is the job description for the position the candidate is applying for:
        {fiche_poste_content}

        Ask relevant questions, one at a time, as in a real interview.
        Wait for the user's response before proceeding.
        """
    elif langue.strip() == "3":
        context = f"""
        Eres un reclutador de RRHH realizando una entrevista de trabajo.
        Aquí está el contenido del CV del candidato:
        {cv_content}

        Aquí está la descripción del puesto para el que el candidato está postulando:
        {fiche_poste_content}

        Haz preguntas relevantes, una por una, como en una entrevista real.
        Espera la respuesta del usuario antes de continuar.
        """
    elif langue.strip() == "4":
        context = f"""
        Du bist ein HR-Recruiter und führst ein Vorstellungsgespräch.
        Hier ist der Inhalt des Lebenslaufs des Kandidaten:
        {cv_content}

        Hier ist die Stellenbeschreibung für die Position, für die sich der Kandidat bewirbt:
        {fiche_poste_content}

        Stelle relevante Fragen, eine nach der anderen, wie in einem echten Vorstellungsgespräch.
        Warte auf die Antwort des Benutzers, bevor du fortfährst.
        """
    else:
        print("Choix invalide. Fin du programme.")
        exit()

    messages = [HumanMessage(content=context)]

    mode = input("Choisissez le mode : [1] Vocal  [2] Texte\nVotre choix : ")

    if mode.strip() == "1":
        chatbot_vocal(messages, cv_content, fiche_poste_content)
    elif mode.strip() == "2":
        chatbot_textuel(messages, cv_content, fiche_poste_content)
    else:
        print("Choix invalide. Fin du programme.")
