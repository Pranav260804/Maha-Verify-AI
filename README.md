# Maha Verify AI - Real Estate Document Auditor
## AI-Powered Due Diligence with RERA Integration

![Status](https://img.shields.io/badge/Status-Ready%20for%20Setup-brightgreen) 
![Version](https://img.shields.io/badge/Version-1.0.0-blue) 
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)

Maha Verify AI is a sophisticated web application designed to automate due diligence on real estate projects in Maharashtra. By leveraging AI-powered document analysis and real-time verification against the live MahaRERA portal, it empowers buyers, investors, and legal professionals with swift, accurate risk assessments, ensuring complete transparency before property investments.

---

## 📸 Interface Previews


![Dashboard / Smart Audit](docs/<img width="1919" height="1079" alt="Screenshot 2026-04-17 112406" src="https://github.com/user-attachments/assets/5be4ad81-798d-4b7a-b9dd-555fa7a11ba1" />
)

![RERA Deep Search Results](docs/<img width="1919" height="1079" alt="Screenshot 2026-04-17 112417" src="https://github.com/user-attachments/assets/773a2234-2234-4035-8493-f5eb7d6e5909" />
)


![Automated Legal Opinion](docs/<img width="1919" height="1079" alt="Screenshot 2026-04-17 112729" src="https://github.com/user-attachments/assets/96d4ce59-99e5-44fa-af31-79da3d49e58a" />
)


---

## ✨ Features

| Feature | Status | Details |
|---------|--------|---------|
| **Smart Audit** | ✅ Complete | Upload Project Registration Certificates for AI-powered verification against live MahaRERA records. |
| **Deep Search** | ✅ Complete | Instantly query the MahaRERA database by RERA registration number. |
| **Search History** | ✅ Complete | Track all previous audits and searches for easy reference. |
| **Google OAuth** | ✅ Complete | Secure and seamless user authentication. |
| **AI Analysis** | ✅ Integrated | OpenAI-powered intelligence for highly accurate document text extraction. |
| **RERA Integration** | ✅ Ready | Live automated portal scraping with robust 2Captcha resolution handling. |
| **Risk Assessment** | ✅ Complete | Automatic "Good to Buy" or "Risk" advisory powered by integrated Legal AI analysis. |
| **Responsive Design** | ✅ Complete | Clean UI dynamically optimized for Mobile, Tablet, and Desktop. |

## 🚀 Quick Start

### 1. Run Setup Script (Recommended)

**Windows:**
```bash
quickstart.bat
```

**macOS/Linux:**
```bash
bash quickstart.sh
```

### 2. Configure `.env` File
```bash
cp .env.example .env
# Edit .env with your actual API keys (Google OAuth, OpenAI, and 2Captcha)
```

### 3. Start Server
```bash
python quickstart.py
# The application will automatically start. Visit http://localhost:8000
```

## 📋 Tech Stack

**Frontend:**
- HTML5 / CSS3 / Vanilla JavaScript (ES6+)
- Responsive, intuitive User Interface
- Real-time DOM state management
- Seamless drag-and-drop file upload integration

**Backend:**
- FastAPI 0.104.1 (Python asynchronous web framework)
- SQLAlchemy ORM (SQLite/PostgreSQL compatible)
- Google OAuth 2.0 integration
- OpenAI GPT-3.5 API for document parsing and structural analysis
- Selenium WebDriver for secure, undetectable RERA portal automation

**External APIs:**
- Google Cloud OAuth Service
- OpenAI GPT API
- MahaRERA Public Portal
- 2Captcha Verification API

## 📁 Project Structure

```text
Maha Verify AI/
├── index.html                # Frontend UI
├── style.css                 # Styling & responsive design
├── app.js                    # Core frontend logic & AI processing simulation
├── requirements.txt          # Required Python dependencies
├── .env.example              # Environment variables template
├── SETUP.md                  # Comprehensive setup guide
├── README.md                 # This file
├── quickstart.py             # Quick start script
├── quickstart.sh             # macOS/Linux initial setup
├── quickstart.bat            # Windows initial setup
│
└── backend/
    ├── main.py               # Core FastAPI entry point
    ├── config.py             # Configuration & environment variable bindings
    ├── auth.py               # Google OAuth & session handling
    ├── database.py           # SQLAlchemy database models & schemas
    │
    ├── routes/
    │   ├── __init__.py
    │   ├── document.py       # API endpoints for document analysis
    │   ├── rera.py           # API endpoints for RERA portal interactions
    │   └── history.py        # API endpoints for retrieving search history
    │
    └── services/
        ├── __init__.py
        └── rera_scraper.py   # Selenium RERA scraping integrated with 2Captcha
```

## ⚙️ Setting Up

### Prerequisites

- Python 3.8+
- Active Google Cloud project with OAuth API enabled
- Valid OpenAI API Key
- Valid 2Captcha API Key
- Tesseract OCR (Required for legacy/image-based PDF extraction)

### 1. Clone & Setup Virtual Environment

```bash
# Clone or create project folder
git clone https://github.com/Pranav260804/Maha-Verify-AI.git
cd Maha-Verify-AI

# Create python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Credentials

Ensure your `.env` is fully populated. It should look like this:

```env
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# 2Captcha Configuration
CAPTCHA_API_KEY=your_2captcha_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./maha_verify.db

# Server Secret
SECRET_KEY=your_secure_randomly_generated_key
DEBUG=True
```

### 4. Run the Application

Start the backend server using Uvicorn:

```bash
python -m uvicorn backend.main:app --reload --port 8000
```
*Frontend is served locally. Access the application by navigating to:*
[http://localhost:8000](http://localhost:8000)

## 🔍 Core Workflows

### Smart Document Audit
- **Strict Guidelines**: The system requires users to upload the official **Project Registration Certificate** to ensure accuracy against live portal databases.
- **Data Flow**: Utilizes Tesseract OCR for text ingestion → OpenAI formats the legal schema structure → Selenium securely logs into the live MahaRERA portal → Verification executes matching developers, completion dates (considering official portal revisions/extensions), and registered litigations.
- **Report Generation**: Automatically formulates a "Legal Real Estate Advisor" summary based on discrepancies and flags identified in the cross-reference audit.

### Deep Deep Search 
- Allows standalone queries by verifying known RERA IDs directly against the backend scraping service without a document upload.

## 🚧 Expected Future Enhancements
1. Extended scraping configurations for complex legal litigation documents.
2. Court database APIs (e.g., e-Courts India) integrations.
3. React Native Mobile Application port for quick on-site verifications.
4. Scale up the scraping micro-service onto isolated cloud containers (GCP/AWS).

## 🛡️ License & Disclaimers

**MIT License** - Open for personal use and modification. See [LICENSE](LICENSE) file for more specifications.

**Disclaimer:** *This application is intended strictly for informational risk-assessment purposes. Maha Verify AI is actively fetching data securely but should not overwrite or act as a total substitute for professional, human-bound legal counsel.*

---
**Last Updated:** April 2026 | **Version:** 1.0.0
