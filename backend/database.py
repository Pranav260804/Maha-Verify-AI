from sqlalchemy import create_engine, Column, String, DateTime, Integer, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from backend.config import settings

# Database setup
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    google_id = Column(String, unique=True)
    picture = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)

class AuditRecord(Base):
    __tablename__ = "audit_history"

    id = Column(String, primary_key=True, index=True)
    user_email = Column(String, index=True)
    audit_type = Column(String)  # 'document_audit' or 'rera_search'
    file_name = Column(String, nullable=True)
    rera_number = Column(String, index=True, nullable=True)
    project_name = Column(String)
    developer_name = Column(String)
    recommendation = Column(String)  # 'Good to Buy' or 'Risk'
    issues = Column(JSON, default=list)
    full_report = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")

def get_db():
    """Get database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_user(email: str, name: str, google_id: str, picture: str = None):
    """Create new user"""
    db = SessionLocal()
    try:
        user = User(
            id=google_id,
            email=email,
            name=name,
            google_id=google_id,
            picture=picture
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
        return None
    finally:
        db.close()

def get_user_by_email(email: str):
    """Get user by email"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        return user
    finally:
        db.close()

def save_audit_record(user_email: str, audit_data: dict):
    """Save audit record to database"""
    db = SessionLocal()
    try:
        import uuid
        record = AuditRecord(
            id=str(uuid.uuid4()),
            user_email=user_email,
            audit_type=audit_data.get("type"),
            file_name=audit_data.get("file_name"),
            rera_number=audit_data.get("rera_number"),
            project_name=audit_data.get("project_name"),
            developer_name=audit_data.get("developer_name"),
            recommendation=audit_data.get("recommendation"),
            issues=audit_data.get("issues", []),
            full_report=audit_data
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except Exception as e:
        db.rollback()
        print(f"Error saving audit record: {e}")
        return None
    finally:
        db.close()

def get_user_history(email: str, limit: int = 50):
    """Get user's audit history"""
    db = SessionLocal()
    try:
        records = db.query(AuditRecord).filter(
            AuditRecord.user_email == email
        ).order_by(AuditRecord.created_at.desc()).limit(limit).all()
        return records
    finally:
        db.close()
