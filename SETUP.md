# Maha Verify AI - Setup & Installation Guide

## 🚀 Project Overview
Maha Verify AI is an AI-powered real estate document auditor that:
- Analyzes property documents (PDF, JPG, PNG) using OCR
- Extracts key information via OpenAI GPT
- Verifies against MahaRERA portal data (with automatic CAPTCHA solving)
- Provides "Good to Buy" or "Risk" recommendations
- Maintains audit history for each user

---

## 📋 System Requirements

- **Python**: 3.8+
- **Node.js**: 14+ (for frontend, if needed)
- **Tesseract OCR**: System binary required
- **ChromeDriver**: For RERA portal scraping
- **API Keys**: Google OAuth, OpenAI, 2Captcha

---

## 🔧 Installation Steps

### 1. Clone/Extract Project
```bash
cd "Maha Verify AI"
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt

# Additional for OCR support
pip install python-dotenv pillow
```

### 4. Install System Dependencies

#### Windows
```bash
# Download Tesseract OCR installer from:
# https://github.com/UB-Mannheim/tesseract/wiki
# Run the installer

# Download ChromeDriver:
# https://chromedriver.chromium.org/
# Add to PATH or backend/drivers/
```

#### macOS
```bash
brew install tesseract
brew install chromedriver
```

#### Linux (Ubuntu)
```bash
sudo apt-get install tesseract-ocr
# ChromeDriver via snapcraft or manual download
```

### 5. Configure Environment
```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your API keys:
# - GOOGLE_CLIENT_ID/SECRET (from Google Cloud Console)
# - OPENAI_API_KEY (from OpenAI)
# - CAPTCHA_API_KEY (from 2Captcha)
```

### 6. Initialize Database
```bash
# Run from project root
python -c "from backend.database import init_db; init_db()"
```

### 7. Start Backend Server
```bash
# Development
uvicorn backend.main:app --reload --port 8000

# Production
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 8. Access Application
- Frontend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

## 🔑 API Keys Setup

### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create OAuth 2.0 credentials (Web Application)
3. Authorized redirect URIs: `http://localhost:8000/auth/callback`
4. Copy Client ID & Secret to `.env`

### OpenAI
1. Sign up at [OpenAI API](https://platform.openai.com)
2. Generate API key
3. Add to `.env` as `OPENAI_API_KEY`

### 2Captcha
1. Register at [2Captcha](https://2captcha.com)
2. Fund your account
3. Add API key to `.env` as `CAPTCHA_API_KEY`

---

## 📁 Project Structure

```
Maha Verify AI/
├── index.html              # Frontend UI
├── style.css               # Styling (dark theme)
├── app.js                  # Frontend logic
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
│
└── backend/
    ├── main.py             # FastAPI app entry point
    ├── config.py           # Configuration settings
    ├── auth.py             # Google OAuth & JWT
    ├── database.py         # SQLAlchemy models
    │
    ├── routes/
    │   ├── document.py     # PDF/Image analysis
    │   ├── rera.py         # RERA portal queries
    │   └── history.py      # Audit history
    │
    └── services/
        └── rera_scraper.py # RERA scraping with CAPTCHA
```

---

## 🎯 Frontend Features

### Smart Audit Tab
- Drag-and-drop document upload
- File validation and preview
- AI-powered document analysis
- Risk assessment with detailed findings
- "Good to Buy" vs "Risk" recommendation

### Deep Search Tab
- Search by RERA registration number
- Fetch live data from MahaRERA portal
- Display project details, developer info, approvals
- Litigation tracking

### Past Reports Tab
- Grid view of all user audits/searches
- Click to expand for details
- Date-based sorting
- Status badges (Good/Risk)

---

## 🔄 API Endpoints

### Authentication
- `GET /auth/login` - Start OAuth flow
- `GET /auth/callback` - OAuth callback
- `GET /auth/verify` - Verify token validity
- `POST /auth/logout` - Logout user

### Document Analysis
- `POST /api/analyze-document` - Upload & analyze document
- Returns: RERA number, project name, developer, completion date

### RERA Data
- `GET /api/rera-data?rera_number={number}` - Fetch project details
- `GET /api/rera-search?query={query}` - Search RERA projects
- `GET /api/rera-litigations?rera_number={number}` - Get litigation info

### History
- `GET /api/history` - Get user's audit history (paginated)
- `POST /api/history` - Save new audit/search record
- `GET /api/history/{record_id}` - Get detailed record
- `DELETE /api/history/{record_id}` - Delete record

---

## 🛡️ Security Considerations

1. **Change SECRET_KEY**: Update in .env for production
2. **HTTPS**: Enable in production
3. **CORS**: Restrict to known domains
4. **Rate Limiting**: Add per user/IP
5. **Input Validation**: All endpoints validate inputs
6. **Token Expiry**: JWTs expire after 24 hours

---

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Tesseract not found
- Ensure Tesseract OCR is installed and in PATH
- Or set path in code: `pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`

### CAPTCHA solving fails
- Verify 2Captcha API key is correct
- Check account has sufficient balance
- Ensure internet connectivity

### Database errors
```bash
# Reset database
rm maha_verify.db
python -c "from backend.database import init_db; init_db()"
```

---

## 📊 Audit Logic

1. **Upload Document** → Validate file type/size
2. **Extract Text** → Use Tesseract OCR for images, PDF-to-image first
3. **AI Analysis** → OpenAI extracts RERA number, developer, completion date
4. **Fetch RERA Data** → Query MahaRERA portal (with auto CAPTCHA solving)
5. **Compare & Validate** → Check developer match, date consistency, litigations
6. **Generate Report** → Output recommendation + detailed findings
7. **Save History** → Store in database with user linkage

---

## 🚀 Next Steps

1. Add more document validation rules
2. Implement WebSocket for real-time progress updates
3. Add report PDF export
4. Implement advanced litigation search
5. Add developer reputation scoring
6. Create admin dashboard for analytics

