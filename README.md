# Carrier_Conversation – Personal AI Agent

A **personal AI-powered career assistant** built with **Groq LLMs** and **Gradio**, designed to answer questions about my background, skills, and experience using my resume and LinkedIn data.
The application supports **tool calling**, **PDF ingestion**, and optional **Pushover notifications**, and is deployable on **Hugging Face Spaces**.

---

## 🚀 Features

* AI chatbot representing my professional profile
* Reads and understands resume / LinkedIn PDF
* Tool calling for:

  * Recording user contact details
  * Logging unanswered questions
* Optional real-time notifications via Pushover
* Clean Gradio chat interface
* Hugging Face Spaces–ready deployment

---

## 🧠 Tech Stack

* **LLM**: Groq (LLaMA 3.1 – OpenAI-compatible API)
* **Frontend**: Gradio
* **Backend**: Python
* **PDF Parsing**: PyPDF
* **Notifications**: Pushover (optional)

---

## 📁 Project Structure

```
.
├── app.py
├── requirements.txt
├── README.md
└── me/
    ├── linkedin.pdf
    └── summary.txt
```

---

## 🔧 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/career-agent.git
cd career-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

The app uses environment variables for API access.

### Required

* `GROQ_API_KEY` – Groq API key

### Optional (for notifications)

* `PUSHOVER_USER`
* `PUSHOVER_TOKEN`

#### Local setup (optional)

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
PUSHOVER_USER=your_user_key
PUSHOVER_TOKEN=your_app_token
```

⚠️ **Note:** Hugging Face Spaces does **not** support `.env` files. Use **Spaces → Settings → Secrets** instead.

---

## ▶️ Running Locally

```bash
python app.py
```

The app will launch a Gradio interface in your browser.

---

## 🤗 Deploying to Hugging Face Spaces

1. Create a **Gradio Space**
2. Upload:

   * `app.py`
   * `requirements.txt`
   * `me/` folder
3. Add secrets in **Settings → Secrets**
4. The app will auto-build and launch

---

## 🛠 Tool Calling Capabilities

The assistant can:

* Store visitor contact information (email, name, notes)
* Log unanswered or unclear questions
* Trigger push notifications (if enabled)

---

## 📌 Notes

* Ensure `me/linkedin.pdf` exists before running
* File paths are **case-sensitive**
* Pushover is optional and can be removed safely

---

## 📄 License

This project is released under the **MIT License**.

---

## 🙌 Acknowledgements

* Groq for ultra-fast LLM inference
* Gradio for rapid UI development
* OpenAI API compatibility standard
