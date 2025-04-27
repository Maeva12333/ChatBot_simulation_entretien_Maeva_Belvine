# Chatbot d'entretien RH

## Contexte

Ce projet consiste à créer un chatbot d'entretien RH conçu pour aider les candidats à se préparer à un entretien d'embauche en fonction de leur CV et de la fiche de poste pour laquelle ils postulent. Le chatbot analyse les informations du CV et de la fiche de poste, puis génère une série de questions pertinentes pour l'entretien. Après chaque réponse de l'utilisateur, il génère une question suivante, tout comme un entretien réel. En fin de session, le chatbot fournit un feedback sur la pertinence du CV par rapport à la fiche de poste, ainsi que des retours sur la qualité des réponses données pendant l'entretien.

Ce projet implémente un chatbot d'entretien RH utilisant un modèle de langage (LLM) pour aider les candidats à se préparer à un entretien d'embauche. Il permet d'interagir avec le modèle à la fois via une interface Streamlit ou en mode terminal avec la reconnaissance vocale et la synthèse vocale.

## Fonctionnalités

### 1. Mode Streamlit (Interface Graphique)
- **Chargement des fichiers :** Le candidat charge son CV et la fiche de poste pour laquelle il postule. 
- **Entretien en ligne :** Le chatbot interroge le candidat et lui pose des questions pertinentes liées à la fiche de poste et au CV.
- **Feedback :** À la fin de l'entretien, un retour est généré, évaluant la pertinence du CV par rapport à la fiche de poste et la qualité des réponses du candidat.

### 2. Mode Terminal (Interface en ligne de commande)
- Le programme propose également un mode d'entretien via la ligne de commande pour les utilisateurs préférant interagir sans interface graphique. 
- **Vocal ou texte :** Les utilisateurs peuvent choisir d'interagir via la voix ou en texte uniquement. 
  - **Mode vocal :** Utilise la reconnaissance vocale et la synthèse vocale pour rendre l'entretien plus interactif.
  - **Mode texte :** Les utilisateurs répondent aux questions du chatbot en tapant leurs réponses dans le terminal.


## Prérequis

Avant de pouvoir exécuter ce projet, vous devez vous assurer que vous avez installé les dépendances suivantes :

- Python 3.x
- Streamlit
- PyPDF2
- python-docx
- pyttsx3
- speech_recognition
- Langchain

## Installation des dépendances

1. Ajouter votre clé API pour le modèle LLM dans le fichier `chatbot-test.py` (ou dans l'environnement si nécessaire).
   ```python
   os.environ["GROQ_API_KEY"] = "votre_clé_api"
   ```

## Exécution du projet

1. Exécutez l'application avec la commande suivante :
   ```bash
   streamlit run chemin/acces/chatbot-test.py
   ```

2. Une fois l'application démarrée, vous pourrez accéder à l'interface d'entretien RH via votre navigateur web. Vous devrez télécharger votre CV et la fiche de poste pour démarrer l'entretien.

3. L'entretien commence avec la première question du recruteur : "Pouvez-vous vous présenter ?". Répondez à chaque question et à la fin de l'entretien, vous recevrez un feedback détaillé.

## Structure du projet

- **chatbot-test.py** : Fichier principal où le chatbot est exécuté avec Streamlit.
- **chatbot_local.py** : Fichier principal où le chatbot est exécuté à partir du terminal.
- **README.md** : Ce fichier de documentation.

## Contribuer

Si vous souhaitez contribuer à ce projet, vous pouvez :
- Cloner le projet et y ajouter de nouvelles fonctionnalités.
- Créer des issues pour proposer des améliorations.
- Faire des pull requests.

## Auteurs

- **Maeva SIMO KAMWA**
- **Belvine YEMDJO**
  
## Licence

Ce projet est sous licence MIT.
