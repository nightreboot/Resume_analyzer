<div align="center">

<img src="https://img.shields.io/badge/ResumeIQ-ATS%20Analyzer-6366F1?style=for-the-badge&logo=robot&logoColor=white" alt="ResumeIQ"/>

# 🎯 ResumeIQ — AI-Powered ATS Resume Analyzer

**Upload your resume. Paste the job description. Know your score before the recruiter does.**

Powered by **Mistral AI** · **ChromaDB** · **FastAPI** · **LangChain**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=flat-square&logo=chainlink&logoColor=white)](https://langchain.com)
[![Mistral AI](https://img.shields.io/badge/Mistral-AI-FF7000?style=flat-square&logo=mistral&logoColor=white)](https://mistral.ai)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-E8572A?style=flat-square)](https://trychroma.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)

---

<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/main/icons/folder-app.svg" width="80" alt="app icon"/>

*Drop your resume → get an ATS score, skill gap report, and improvement plan in seconds.*

</div>

---

## ✨ What It Does

ResumeIQ is a full-stack AI application that acts as both a **hiring manager** and an **ATS (Applicant Tracking System)**. It:

- 📄 Extracts text from **PDF resumes** or **scanned image resumes** (via OCR)
- 🧠 Embeds your resume into a **vector store** for semantic retrieval
- 🤖 Uses **Mistral AI** to compare your resume against the job description
- 📊 Returns an **ATS Match Score (0–100%)** with detailed breakdown
- 🛠️ Provides **actionable improvement suggestions** and missing keywords

---

## 🖥️ Screenshots

<div align="center">

### Input Panel — Upload & Analyze
```
┌─────────────────────────────────────────────────────────────────┐
│  ⬡ ResumeIQ                                      ATS ANALYZER   │
├──────────────────────────────┬──────────────────────────────────┤
│  01  YOUR RESUME             │  RESULTS                         │
│  ┌──────────────────────┐    │                                  │
│  │  📄 Drop resume here │    │        🎯                        │
│  │  PDF · PNG · JPG     │    │   Upload a resume and add a     │
│  └──────────────────────┘    │   job description to see        │
│                              │   your ATS analysis.            │
│  02  JOB DESCRIPTION         │                                  │
│  ┌──────────────────────┐    │                                  │
│  │ Paste the full JD…   │    │                                  │
│  │                      │    │                                  │
│  └──────────────────────┘    │                                  │
│  [ ▶ Analyze Resume ]        │                                  │
└──────────────────────────────┴──────────────────────────────────┘
```

### Results Panel — ATS Score & Report
```
┌──────────────────────────────────────────────────────────────────┐
│  RESULTS                                                          │
│                                                                   │
│   ╭──────╮   🟢 Strong Match                                      │
│   │  78  │   This resume is well aligned with the job.           │
│   │ /100 │                                                        │
│   ╰──────╯                                                        │
│                                                                   │
│  MATCHED SKILLS                                                   │
│  [Python] [FastAPI] [REST API] [Docker] [PostgreSQL]             │
│                                                                   │
│  MISSING SKILLS                                                   │
│  [Kubernetes] [Redis] [GraphQL]                                  │
│                                                                   │
│  KEYWORDS TO ADD                                                  │
│  [microservices] [CI/CD] [test-driven]                           │
│                                                                   │
│  IMPROVEMENT SUGGESTIONS                                          │
│  › Add quantified achievements (e.g. "reduced latency by 40%")  │
│  › Include Kubernetes experience or mention learning it          │
│                                                                   │
│  FINAL VERDICT                                                    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Strong candidate — minor keyword gaps. Tailor summary   │    │
│  │ section and add missing tech to skills list.            │    │
│  └─────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

</div>

---

## 🏗️ Architecture

```
                        ┌─────────────────────────────────────────┐
                        │            Browser / Frontend            │
                        │         index.html  (HTML/CSS/JS)        │
                        └──────────────────┬──────────────────────┘
                                           │  POST /analyze
                                           │  multipart/form-data
                                           ▼
                        ┌─────────────────────────────────────────┐
                        │          FastAPI  (main.py)              │
                        │                                          │
                        │  ① Validate file type & JD length       │
                        │  ② Save to temp file                    │
                        │  ③ Route to pipeline                    │
                        └──────┬─────────────────────────┬────────┘
                               │                         │
               ┌───────────────▼──────────┐   ┌─────────▼──────────────┐
               │   detail_extractor.py    │   │   cleaning_data.py     │
               │                          │   │                        │
               │  PDF  → PyMuPDF          │   │  Regex clean:          │
               │  IMG  → Tesseract OCR    │──▶│  • strip whitespace   │
               │                          │   │  • remove junk chars  │
               └──────────────────────────┘   └─────────┬──────────────┘
                                                        │ clean text
                                                        ▼
                                          ┌─────────────────────────┐
                                          │     vectore_db.py        │
                                          │                          │
                                          │  chunk_text()            │
                                          │  RecursiveTextSplitter   │
                                          │  chunk=200 / overlap=50  │
                                          │           │              │
                                          │  vector_store()          │
                                          │  HuggingFace Embeddings  │
                                          │  all-MiniLM-L6-v2        │
                                          │           │              │
                                          │  ChromaDB (local)        │
                                          │  MMR Retrieval (k=5)     │
                                          └─────────────┬────────────┘
                                                        │ top-k chunks
                                                        ▼
                                          ┌─────────────────────────┐
                                          │   user_description.py    │
                                          │                          │
                                          │  LangChain LCEL chain:   │
                                          │  PromptTemplate          │
                                          │       │                  │
                                          │  ChatMistralAI           │
                                          │  mistral-small-2603      │
                                          │       │                  │
                                          │  StrOutputParser         │
                                          └─────────────┬────────────┘
                                                        │
                                                        ▼
                                          ┌─────────────────────────┐
                                          │   JSON Response          │
                                          │  { "result": "..." }     │
                                          └─────────────────────────┘
```

---

## 📁 Project Structure

```
resumeiq/
│
├── main.py                    ← 🚀 FastAPI application (entry point)
│
├── core/                      ← 🧠 Business logic
│   ├── __init__.py
│   ├── detail_extractor.py    ← PDF text extraction + OCR
│   ├── cleaning_data.py       ← Regex text cleaner
│   ├── vectore_db.py          ← ChromaDB embed / store / retrieve
│   └── user_description.py   ← Mistral AI LangChain chain
│
├── index.html                 ← 🖥️  Frontend (single-file, no build step)
│
├── .env                       ← 🔑 Your secrets (never commit this)
├── .env.example               ← 📋 Template to copy from
└── requirements.txt           ← 📦 Python dependencies
```

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTML · CSS · Vanilla JS | Single-file UI, drag-and-drop, animated score gauge |
| **Backend** | FastAPI + Uvicorn | REST API, file handling, CORS |
| **Extraction** | PyMuPDF · Tesseract OCR | PDF text extraction + image OCR |
| **Embeddings** | `all-MiniLM-L6-v2` (HuggingFace) | Sentence-level semantic embeddings |
| **Vector Store** | ChromaDB | Local persistent vector store, MMR retrieval |
| **LLM** | Mistral AI (`mistral-small-2603`) | Resume vs JD analysis & scoring |
| **Orchestration** | LangChain LCEL | Prompt → LLM → Parser chain |
| **Config** | python-dotenv | `.env` based secret management |

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Version | Notes |
|------------|---------|-------|
| Python | 3.10+ | Required |
| Tesseract OCR | Any | For image resumes |
| Mistral API Key | — | [Get one free](https://console.mistral.ai/) |

---

### Step 1 — Install Tesseract OCR

Tesseract is needed to extract text from PNG/JPG resume files.

```bash
# 🍎 macOS
brew install tesseract

# 🐧 Ubuntu / Debian
sudo apt update && sudo apt install tesseract-ocr -y

# 🪟 Windows
# Download the installer from:
# https://github.com/UB-Mannheim/tesseract/wiki
# Then add to PATH
```

---

### Step 2 — Clone & set up Python environment

```bash
# Clone the repo
git clone https://github.com/your-username/resumeiq.git
cd resumeiq

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

---

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

> 💡 First run downloads the `all-MiniLM-L6-v2` model (~90 MB). This is cached locally after the first download.

---

### Step 4 — Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and add your key:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

> 🔑 Get your free Mistral API key at [console.mistral.ai](https://console.mistral.ai/)

---

### Step 5 — Run the backend

```bash
uvicorn main:app --reload --port 8000
```

You should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

---

### Step 6 — Open the frontend

Open `index.html` in your browser:
- **Double-click** `index.html`, or
- Use **VS Code Live Server** extension, or
- Serve with Python: `python -m http.server 3000` then visit `http://localhost:3000`

---

## 🔌 API Reference

### `GET /`
Health check.

**Response:**
```json
{ "status": "ok", "message": "ResumeIQ API is running." }
```

---

### `POST /analyze`
Upload a resume and job description for ATS analysis.

**Request** — `multipart/form-data`:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | File | ✅ | Resume (`.pdf`, `.png`, `.jpg`, `.jpeg`) |
| `job_description` | String | ✅ | Full job description text (min 20 chars) |

**Response `200 OK`:**
```json
{
  "result": "ATS Score: 78%\n\nMatched Skills:\n- Python\n- FastAPI\n..."
}
```

**Error Responses:**

| Code | Reason |
|------|--------|
| `400` | Unsupported file type or JD too short |
| `422` | Could not extract text from file |
| `500` | Embedding or LLM failure |

---

### Interactive Docs

Once the server is running, visit:

```
http://localhost:8000/docs       ← Swagger UI
http://localhost:8000/redoc      ← ReDoc
```

---

## 📊 Analysis Output Format

The AI returns a structured plain-text report:

```
ATS Score: 78%

Matched Skills:
- Python
- FastAPI
- PostgreSQL

Missing Skills:
- Kubernetes
- Redis

Strengths:
- Strong backend experience with Python and REST APIs
- Relevant project experience in microservices

Weaknesses:
- No mention of containerization beyond Docker
- Missing cloud platform experience

Improvement Suggestions:
- Add "Kubernetes" and "Helm" to skills section
- Quantify achievements (e.g. "reduced API latency by 35%")
- Mention CI/CD pipelines (GitHub Actions, Jenkins)

Keywords to Add:
- microservices
- distributed systems
- test-driven development

Final Verdict:
Strong candidate with solid Python backend skills. Minor keyword
gaps around orchestration and cloud. Tailoring the summary and
skills section should push the ATS score above 85%.
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| `tesseract not found` | Install Tesseract and ensure it's on your `PATH` |
| `MISTRAL_API_KEY` error | Make sure `.env` exists with the correct key |
| Empty text extraction | PDF may be image-only — try a text-selectable PDF |
| ChromaDB errors | Delete the `Chroma/` folder and re-run to reset the store |
| CORS error in browser | Ensure `uvicorn` is running on port `8000` |
| Slow first run | HuggingFace model is downloading (~90 MB), wait for it |

---

## 🗺️ Roadmap

- [ ] Multi-resume batch comparison
- [ ] Resume rewrite suggestions (inline edits)
- [ ] Export report as PDF
- [ ] User accounts & history
- [ ] LinkedIn job scraping integration
- [ ] Docker Compose deployment

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "feat: add my feature"`
4. Push to branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built with ❤️ using **FastAPI** · **Mistral AI** · **ChromaDB** · **LangChain**

⭐ Star this repo if it helped you land the job!

</div>
