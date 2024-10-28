from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db import Base


class Message(Base):
    __tablename__ = "Сообщения"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    sender = relationship("User", foreign_keys="Message.sender_id")
    recipient = relationship("User", foreign_keys="Message.recipient_id")
