from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, func
from datetime import datetime
from sqlalchemy.orm import relationship
from Flask_doc.docs.models.database import db


class Documents(db.Model):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, default="", server_default="")
    body = Column(Text, nullable=False, default="", server_default="")
    dt_created = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    version = Column(Text, nullable=False, default="", server_default="")
    id_main = Column(Integer)
