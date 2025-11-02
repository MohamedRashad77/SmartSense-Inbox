from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class SMS(Base):
    __tablename__ = 'sms'

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    body = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Classification fields
    category = Column(String, index=True)  # offers, finance, travel, otp, transactional, spam
    is_threat = Column(Boolean, default=False, index=True)
    threat_reason = Column(String, nullable=True)
    
    # Extracted entities
    urls = Column(JSON, nullable=True)  # List of URLs found
    has_money_request = Column(Boolean, default=False)
    has_otp = Column(Boolean, default=False)
    
    # Metadata
    message_id = Column(String, unique=True, nullable=True)
    
    def __repr__(self):
        return f"<SMS(id={self.id}, sender='{self.sender}', category='{self.category}', is_threat={self.is_threat})>"