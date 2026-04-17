"""
Audit History Routes
Manages user search and audit history with database persistence
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
from typing import List, Optional
from ..config import settings
from ..auth import verify_token
from ..database import get_db, AuditRecord

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/history")
async def get_user_history(
    skip: int = 0,
    limit: int = 50,
    user_id: str = Depends(verify_token),
    db = Depends(get_db)
):
    """
    Retrieve user's audit and search history
    Supports pagination for better performance
    """
    try:
        # Query history from database
        records = db.query(AuditRecord).filter(
            AuditRecord.user_id == user_id
        ).order_by(
            AuditRecord.created_at.desc()
        ).offset(skip).limit(limit).all()

        history_list = []
        for record in records:
            history_list.append({
                "id": record.id,
                "type": record.record_type,  # 'audit' or 'search'
                "file_name": record.file_name,
                "rera_number": record.rera_number,
                "project_name": record.project_name,
                "recommendation": record.recommendation,
                "timestamp": record.created_at.isoformat()
            })

        return JSONResponse(content={
            "status": "success",
            "total": len(history_list),
            "history": history_list
        })

    except Exception as e:
        logger.error(f"History retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")


@router.post("/history")
async def save_audit_record(
    record_data: dict,
    user_id: str = Depends(verify_token),
    db = Depends(get_db)
):
    """
    Save audit or search record to history
    """
    try:
        # Create new record
        new_record = AuditRecord(
            user_id=user_id,
            record_type=record_data.get("type"),  # 'audit' or 'search'
            file_name=record_data.get("fileName"),
            rera_number=record_data.get("reraNumber"),
            project_name=record_data.get("projectName"),
            recommendation=record_data.get("result"),
            created_at=datetime.utcnow()
        )

        db.add(new_record)
        db.commit()
        db.refresh(new_record)

        return JSONResponse(content={
            "status": "success",
            "message": "Record saved successfully",
            "record_id": new_record.id
        })

    except Exception as e:
        logger.error(f"History save error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save history: {str(e)}")


@router.get("/history/{record_id}")
async def get_history_detail(
    record_id: int,
    user_id: str = Depends(verify_token),
    db = Depends(get_db)
):
    """
    Retrieve detailed information about a specific audit/search
    """
    try:
        record = db.query(AuditRecord).filter(
            AuditRecord.id == record_id,
            AuditRecord.user_id == user_id
        ).first()

        if not record:
            raise HTTPException(status_code=404, detail="Record not found")

        return JSONResponse(content={
            "status": "success",
            "record": {
                "id": record.id,
                "type": record.record_type,
                "file_name": record.file_name,
                "rera_number": record.rera_number,
                "project_name": record.project_name,
                "recommendation": record.recommendation,
                "details": record.details,  # Full JSON details
                "timestamp": record.created_at.isoformat()
            }
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"History detail error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve record: {str(e)}")


@router.delete("/history/{record_id}")
async def delete_history_record(
    record_id: int,
    user_id: str = Depends(verify_token),
    db = Depends(get_db)
):
    """
    Delete a specific audit/search record from history
    """
    try:
        record = db.query(AuditRecord).filter(
            AuditRecord.id == record_id,
            AuditRecord.user_id == user_id
        ).first()

        if not record:
            raise HTTPException(status_code=404, detail="Record not found")

        db.delete(record)
        db.commit()

        return JSONResponse(content={
            "status": "success",
            "message": "Record deleted successfully"
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"History delete error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete record: {str(e)}")
