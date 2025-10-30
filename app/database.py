import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DB_URL = os.getenv("DATABASE_URL", "sqlite:////data/plant_ai.db")  # persist on Render disk
Base = declarative_base()
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    species_name = Column(String, index=True)
    confidence_score = Column(Float)
    image_path = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    flagged_unsure = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)
