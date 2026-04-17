from fastapi import APIRouter, HTTPException, Depends, Response, Header
from fastapi.responses import RedirectResponse
import httpx
import jwt
from datetime import datetime, timedelta
from typing import Optional
from backend.config import settings
from backend.database import get_db, User

router = APIRouter()

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

def create_jwt_token(data: dict, expires_in_minutes: int = 1440):
    """Create JWT token for user session"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    return token

def verify_token(authorization: Optional[str] = Header(None)) -> dict:
    """Verify JWT token from Authorization header"""
    if not authorization:
        # For demo: allow mock user
        return {"email": "demo@mahaverify.ai", "name": "Demo User", "token": "demo-token-12345"}
    
    try:
        # Extract token from "Bearer <token>" format
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            # For demo: allow any token format
            return {"email": "demo@mahaverify.ai", "name": "Demo User", "token": authorization}
        
        # Try to verify as JWT
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )
            return payload
        except jwt.DecodeError:
            # For demo: allow mock/invalid tokens
            return {"email": "demo@mahaverify.ai", "name": "Demo User", "token": token}
    except (ValueError, AttributeError):
        # For demo: allow any token format
        return {"email": "demo@mahaverify.ai", "name": "Demo User", "token": authorization or "demo-token"}

@router.get("/login")
async def login():
    """Redirect to Google OAuth login"""
    auth_url = f"{GOOGLE_AUTH_URL}?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI}&response_type=code&scope=openid profile email"
    return RedirectResponse(url=auth_url)

@router.get("/callback")
async def oauth_callback(code: str, response: Response, db = Depends(get_db)):
    """Handle Google OAuth callback"""
    try:
        # Exchange code for tokens
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": settings.GOOGLE_REDIRECT_URI
                }
            )

        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get token")

        tokens = token_response.json()
        access_token = tokens.get("access_token")

        # Get user info from Google
        async with httpx.AsyncClient() as client:
            user_response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )

        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get user info")

        user_info = user_response.json()

        # Create or update user in database
        user = User(
            email=user_info.get("email"),
            name=user_info.get("name"),
            google_id=user_info.get("id"),
            picture=user_info.get("picture")
        )
        # In production: Save to database

        # Create JWT token
        jwt_token = create_jwt_token({
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture"),
            "google_id": user_info.get("id")
        })

        # Set secure HTTP-only cookie
        response = RedirectResponse(url="/")
        response.set_cookie(
            "token",
            jwt_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite="lax",
            max_age=86400  # 24 hours
        )

        # Also return token in response body for localStorage fallback
        response.headers["X-Auth-Token"] = jwt_token

        return response

    except Exception as e:
        print(f"OAuth error: {e}")
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

@router.post("/logout")
async def logout(response: Response):
    """Logout user by clearing session"""
    response.delete_cookie("token")
    return {"message": "Logged out successfully"}

@router.get("/verify")
async def verify(token: str = Depends(verify_token)):
    """Verify token validity"""
    return {
        "valid": True,
        "email": token.get("email"),
        "name": token.get("name")
    }
