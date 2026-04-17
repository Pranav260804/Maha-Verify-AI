@echo off
cd /d "c:\Users\ASUS\OneDrive\Desktop\Projects\Maha Verify AI"
call .\venv\Scripts\activate.bat
python -m uvicorn backend.main:app --reload --port 8000
pause
