# Maha Verify AI - Real Estate Document Auditor
## AI-Powered Due Diligence with RERA Integration

![Status](https://img.shields.io/badge/Status-Ready%20for%20Setup-brightgreen) 
![Version](https://img.shields.io/badge/Version-1.0.0-blue) 
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)

A sophisticated web application for automated due diligence on real estate projects in Maharashtra using AI-powered document analysis and RERA database verification.

## ✨ Features

| Feature | Status | Details |
|---------|--------|---------|
| **Smart Audit** | ✅ Complete | Upload Project Registration Certificate for AI-powered verification against live MahaRERA portal |
| **Deep Search** | ✅ Complete | Query MahaRERA database by RERA registration number |
| **Search History** | ✅ Complete | Track all previous audits and searches |
| **Google OAuth** | ✅ Complete | Secure user authentication |
| **AI Analysis** | ✅ Integrated | OpenAI-powered document text extraction |
| **RERA Integration** | ✅ Ready | Portal scraping with 2Captcha CAPTCHA handling |
| **Risk Assessment** | ✅ Complete | Automatic "Good to Buy" or "Risk" recommendations |
| **Responsive Design** | ✅ Complete | Mobile, Tablet, Desktop optimized |

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
# Edit .env with your API keys
```

### 3. Start Server
```bash
python quickstart.py
# Visit http://localhost:8000
```

## 📋 Tech Stack

**Frontend:**
- HTML5 / CSS3 / Vanilla JavaScript (ES6+)
- Responsive design (Mobile, Tablet, Desktop)
- Real-time UI state management
- Drag-and-drop file upload

**Backend:**
- FastAPI 0.104.1 (Python web framework)
- SQLAlchemy ORM (SQLite/PostgreSQL)
- Google OAuth 2.0 integration
- OpenAI API for document analysis
- Selenium for RERA portal automation

**External APIs:**
- Google Cloud OAuth
- OpenAI GPT (gpt-3.5-turbo)
- MahaRERA Portal
- 2Captcha API

## 📁 Project Structure

```
Maha Verify AI/
├── index.html                # Frontend UI (complete)
├── style.css                 # Styling & responsive (complete)
├── app.js                    # Frontend logic (complete)
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── SETUP.md                  # Setup guide
├── README.md                 # This file
├── quickstart.py             # Quick start script
├── quickstart.sh             # macOS/Linux setup
├── quickstart.bat            # Windows setup
│
└── backend/
    ├── main.py               # FastAPI entry point
    ├── config.py             # Configuration & env vars
    ├── auth.py               # Google OAuth & JWT
    ├── database.py           # SQLAlchemy models
    │
    ├── routes/
    │   ├── __init__.py        # Routes package
    │   ├── document.py        # Document analysis endpoints
    │   ├── rera.py            # RERA portal endpoints
    │   └── history.py         # Audit history endpoints
    │
    └── services/
        ├── __init__.py        # Services package
        └── rera_scraper.py    # RERA scraping with 2Captcha
```
│   ├── database.py      # Database models & queries
│   └── schemas.py       # Request/Response schemas
└── README.md            # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js (for future frontend build tools)
- Google Cloud project with OAuth credentials
- OpenAI API key
- 2Captcha API key
- Tesseract OCR (for image text extraction)

### 1. Clone & Setup Virtual Environment

```bash
# Create project folder
mkdir maha-verify-ai
cd maha-verify-ai

# Create virtual environment
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

### 3. Configure Google Cloud OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Google Identity Service
   - Google OAuth 2.0

4. Create OAuth 2.0 credentials:
   - Go to "Credentials"
   - Create "OAuth 2.0 Client IDs"
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8000/auth/callback`
   - Copy Client ID and Client Secret

5. Create `.env` file in project root:

```env
# Google OAuth
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback

# OpenAI
OPENAI_API_KEY=your_openai_api_key

# 2Captcha
CAPTCHA_API_KEY=your_2captcha_key

# Database
DATABASE_URL=sqlite:///./test.db
# Or Firestore: firebase://your-project-id

# Server
SECRET_KEY=your_secret_key_for_sessions
DEBUG=True
```

### 4. Install System Dependencies

**For Windows:**
```bash
# Install Tesseract OCR
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Then add to PATH
```

**For macOS:**
```bash
brew install tesseract
```

**For Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

### 5. Run the Application

```bash
# Start the backend server
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Frontend is served at:
# http://localhost:8000
```

## API Endpoints

### Authentication
- `GET /auth/login` - Redirect to Google OAuth login
- `GET /auth/callback` - OAuth callback handler
- `POST /auth/logout` - Logout user

### Document Analysis
- `POST /api/analyze-document` - Extract & analyze document
  - Request: `{ "text": "extracted document text" }`
  - Response: `{ "reraNumber": "...", "developerName": "...", ... }`

### RERA Search
- `GET /api/rera-data?reraNumber=P51800000001` - Get RERA project data
  - Response: `{ "projectName": "...", "litigations": 0, ... }`

### User History
- `GET /api/history` - Get user's audit/search history
- `POST /api/history` - Save audit/search record
- `GET /api/history/:id` - Get specific audit report

## Key Features Explained

### Smart Audit Flow

1. **Document Upload** (Max 200MB):
   - **Important:** The system expects the official **Project Registration Certificate** to be uploaded. The uploaded document *must* contain the RERA registration number and essential project details to allow for accurate verification against the live portal.
   - Supported formats: PDF, JPG, PNG, JPEG
   - Client-side validation before upload
   - Drag-and-drop or browse file selection

2. **Text Extraction**:
   - Uses `pdf2image` + `pytesseract` for PDFs
   - Tesseract OCR for image files
   - Extracts text with coordinates for smart search

3. **AI Analysis**:
   - Sends extracted text to OpenAI API
   - Extracts: RERA number, developer name, project name, completion date
   - Identifies potential litigations from document

4. **RERA Verification**:
   - Scrapes MahaRERA portal using Selenium
   - Handles CAPTCHA using 2Captcha API
   - Cross-references extracted data with official records

5. **Report Generation**:
   - Compares document vs. RERA data
   - Flags discrepancies
   - Generates "Good to Buy" or "Risk" recommendation
   - Saves report linked to user's email

### Deep Search (RERA No.)

- Direct lookup by RERA registration number
- Fetches current project status
- Shows developer, timeline, approvals, litigations
- Results saved to user's search history

### Search History

- Displays all past audits and searches
- Linked to user's Google email ID
- Shows date, project/file name, recommendation
- Click to view detailed report

## Authentication Flow

```
User → Login → Google OAuth → Grant Permissions → 
→ Backend Verifies Token → Create Session → 
→ Store in DB with Email ID → Redirect to App
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE,
    name TEXT,
    google_id TEXT,
    created_at TIMESTAMP,
    last_login TIMESTAMP
);
```

### Audit History Table
```sql
CREATE TABLE audit_history (
    id TEXT PRIMARY KEY,
    user_email TEXT,
    audit_type TEXT,  -- 'document_audit' or 'rera_search'
    rera_number TEXT,
    project_name TEXT,
    recommendation TEXT,  -- 'Good to Buy' or 'Risk'
    issues TEXT,  -- JSON array of issues
    created_at TIMESTAMP,
    FOREIGN KEY (user_email) REFERENCES users(email)
);
```

## Error Handling

- **Invalid File Format**: Shows user-friendly message
- **File Size Exceeded**: Prevents upload over 200MB
- **API Failures**: Graceful fallback with user notification
- **RERA Not Found**: Returns "Project not found" message
- **CAPTCHA Issues**: Retries automatically up to 3 times

## Security Considerations

✅ HTTPS only in production
✅ OAuth tokens stored securely (HTTP-only cookies)
✅ No sensitive data in frontend state
✅ Rate limiting on API endpoints
✅ Input validation on all endpoints
✅ SQL injection prevention via ORM/parameterized queries
✅ CORS configured for trusted domains only

## Performance Optimizations

- Frontend caching of search results
- Backend caching of RERA data (24-hour TTL)
- Lazy loading of history records
- Async processing for document analysis
- Database indexing on frequently queried fields

## Troubleshooting

### Issue: "RERA portal login failed"
- Check 2Captcha API key validity
- Verify MahaRERA portal URL hasn't changed
- Check internet connectivity

### Issue: "OCR not working"
- Verify Tesseract is installed and in PATH
- For Windows: Restart terminal after installation
- For macOS/Linux: Check installation with `tesseract --version`

### Issue: "OAuth redirect URI mismatch"
- Ensure Google Cloud Console OAuth URI matches backend redirect
- Check URL doesn't have trailing slash issues

### Issue: "File upload fails"
- Verify file is < 200MB
- Check browser console for specific errors
- Ensure backend `/upload` endpoint is accessible

## Next Steps

1. **Enhanced Litigation Detection**:
   - Integrate with court databases
   - Real-time litigation monitoring

2. **Mobile App**:
   - React Native or Flutter implementation

3. **Advanced Analytics**:
   - Historical trend analysis
   - Risk scoring algorithm improvements

4. **Multi-language Support**:
   - Support for Hindi, Marathi legal documents

5. **Batch Processing**:
   - Upload multiple documents for comparison

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [Project Issues](https://github.com/yourusername/maha-verify-ai/issues)
- Email: support@mahaverify.ai

## Disclaimer

This tool is for informational purposes. Always conduct independent legal review before making real estate decisions. Maha Verify AI is not a substitute for professional legal advice.

---

**Last Updated:** April 2026
**Version:** 1.0.0
