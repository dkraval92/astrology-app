from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from database import Base
import datetime

class KundliRecord(Base):
    __tablename__ = "kundli_records"
    id = Column(Integer, primary key=True, index=True)
    full_name = Column(String(100))
    dob = Column(String(20))
    tob = Column(String(20))
    place = Column(String(100))
    email = Column(String(100))
    mobile = Column(String(20))
    gender = Column(String(10))
    latitude = Column(Float)
    longitude = Column(Float)
    ascendant_sign = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
