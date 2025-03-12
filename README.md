# 🏥 Symptom Checker AI

Symptom Checker AI is a **machine-learning-powered health assistant** that allows users to describe their symptoms and receive potential insights. The system utilizes **Ollama AI (Llama3)** to provide intelligent responses.

## 🚀 Features
- 🤖 AI-powered symptom analysis using **Llama3**
- 🗣️ Chat-based interaction for ease of use
- 📜 Conversation history for tracking past interactions
- 🗑️ Option to delete previous conversations
- 🔐 User authentication for personalized experience
- 📊 SQLite3 database for data management

## 🛠️ Tech Stack
- **Frontend:** [Streamlit](https://streamlit.io/) (for the UI)
- **Backend:** Python (FastAPI for API interactions)
- **AI Model:** [Ollama AI (Llama3)](https://ollama.ai/)
- **Database:** SQLite3 (for storing conversations)
- **Hosting:** Ngrok (for API tunneling)

## 📥 Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/symptom-checker-ai.git
cd symptom-checker-ai
```

2️⃣ Create a Virtual Environment
Set up a virtual environment to manage dependencies:
```bash
python -m venv venv
```
Activate the virtual environment:
  Windows:
  ```bash
    venv\Scripts\activate
  ```

3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

4️⃣ Set Up the Database (SQLite3)
Initialize the database for storing user conversations:

```bash
python initialize_db.py
(Ensure you have an initialize_db.py script that sets up the SQLite3 database.)
```

5️⃣ Run the Application
Start the Symptom Checker AI app:

```bash
streamlit run app.py
```

⚠️ Disclaimer
Symptom Checker AI is an informational tool only and not a substitute for professional medical advice, diagnosis, or treatment.

The AI-generated responses may be inaccurate or incomplete and should not be relied upon for medical decisions.
Always consult a qualified healthcare provider for any medical concerns.
The developers assume no responsibility for decisions made based on this system.
Use at your own risk.
By using this software, you acknowledge and agree to these terms.
