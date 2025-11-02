from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from app.schemas.sms import SMSIngest, SMSResponse, QueryRequest, QueryResponse, DigestResponse
from app.core.database import get_db
from app.models.sms_model import SMS
from app.services.sms_processor import sms_processor
from app.services.llm_client import llm_client

router = APIRouter()

@router.post("/sms", response_model=dict, status_code=200)
async def ingest_sms(payload: SMSIngest, db: Session = Depends(get_db)):
    """Receive and process incoming SMS from forwarder"""
    try:
        # Process message
        processed = sms_processor.process_message(
            sender=payload.sender,
            body=payload.body,
            timestamp=payload.timestamp or datetime.utcnow()
        )
        
        # Create SMS record
        sms = SMS(
            sender=processed['sender'],
            body=processed['body'],
            timestamp=processed['timestamp'],
            category=processed['category'],
            is_threat=processed['is_threat'],
            threat_reason=processed['threat_reason'],
            urls=processed['urls'],
            has_money_request=processed['has_money_request'],
            has_otp=processed['has_otp'],
            message_id=payload.message_id
        )
        
        db.add(sms)
        db.commit()
        db.refresh(sms)
        
        return {
            "status": "success",
            "message_id": sms.id,
            "category": sms.category,
            "is_threat": sms.is_threat
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing SMS: {str(e)}")

@router.get("/messages", response_model=List[SMSResponse])
async def get_messages(
    date_filter: Optional[str] = None,
    category: Optional[str] = None,
    threats_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get filtered SMS messages"""
    try:
        query = db.query(SMS)
        
        # Filter by date
        if date_filter:
            target_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
            # Use datetime range for portability across backends
            start_datetime = datetime.combine(target_date, datetime.min.time())
            end_datetime = datetime.combine(target_date, datetime.max.time())
            query = query.filter(
                SMS.timestamp >= start_datetime,
                SMS.timestamp <= end_datetime
            )
        
        # Filter by category
        if category:
            query = query.filter(SMS.category == category)
        
        # Filter threats
        if threats_only:
            query = query.filter(SMS.is_threat == True)
        
        # Order by timestamp descending
        messages = query.order_by(SMS.timestamp.desc()).all()
        
        return messages
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")

@router.get("/digest", response_model=DigestResponse)
async def get_digest(date_filter: Optional[str] = None, db: Session = Depends(get_db)):
    """Get daily digest of SMS messages"""
    try:
        # Default to today
        if date_filter:
            target_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
        else:
            target_date = date.today()
        
        # Create start and end datetime for the target date
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())
        
        # Get messages for the day using datetime range
        messages = db.query(SMS).filter(
            SMS.timestamp >= start_datetime,
            SMS.timestamp <= end_datetime
        ).all()
        
        # Generate digest
        digest = sms_processor.generate_digest(messages, target_date.strftime("%Y-%m-%d"))
        
        return digest
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating digest: {str(e)}")

@router.post("/query", response_model=QueryResponse)
async def query_messages(request: QueryRequest, db: Session = Depends(get_db)):
    """Answer natural language queries about messages"""
    try:
        # Get messages (filter by date if provided)
        query = db.query(SMS)
        
        if request.date:
            target_date = datetime.strptime(request.date, "%Y-%m-%d").date()
            # Create start and end datetime for the target date
            start_datetime = datetime.combine(target_date, datetime.min.time())
            end_datetime = datetime.combine(target_date, datetime.max.time())
            query = query.filter(
                SMS.timestamp >= start_datetime,
                SMS.timestamp <= end_datetime
            )
        else:
            # Default to last 7 days
            from datetime import timedelta
            week_ago = datetime.utcnow() - timedelta(days=7)
            query = query.filter(SMS.timestamp >= week_ago)
        
        messages = query.order_by(SMS.timestamp.desc()).all()
        
        # Get answer from LLM or fallback
        answer = llm_client.answer_query(request.query, messages)
        
        return {
            "answer": answer,
            "sources": [m.id for m in messages[:5]]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.post("/upload-csv")
async def upload_csv(messages: List[SMSIngest], db: Session = Depends(get_db)):
    """Bulk upload messages from CSV (fallback method)"""
    try:
        count = 0
        for payload in messages:
            processed = sms_processor.process_message(
                sender=payload.sender,
                body=payload.body,
                timestamp=payload.timestamp or datetime.utcnow()
            )
            
            sms = SMS(**processed)
            db.add(sms)
            count += 1
        
        db.commit()
        
        return {
            "status": "success",
            "messages_imported": count
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error uploading CSV: {str(e)}")