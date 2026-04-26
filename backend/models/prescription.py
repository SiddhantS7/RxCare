from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True)
    raw_text = Column(Text)
    medicine = Column(String)
    dosage = Column(String)
    frequency = Column(String)
    confidence = Column(Float)
    explanation = Column(Text)
