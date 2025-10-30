from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from . import database, schemas, inference, utils
from datetime import datetime

app = FastAPI(title="Smart Plant AI Backend", version="2.0")

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/predict", response_model=schemas.PredictionOut)
def predict_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # 1. Save image locally
        image_path = utils.save_uploaded_image(file)

        # 2. Run prediction
        species_name, confidence = inference.predict_image(image_path)

        # 3. Determine if "unsure" (low confidence)
        flagged_unsure = confidence < 0.6

        # 4. Save record to DB
        record = database.Prediction(
            species_name=species_name,
            confidence_score=confidence,
            image_path=image_path,
            flagged_unsure=flagged_unsure,
            timestamp=datetime.utcnow(),
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/records", response_model=list[schemas.PredictionOut])
def get_all_records(db: Session = Depends(get_db)):
    return db.query(database.Prediction).all()

@app.get("/record/{record_id}", response_model=schemas.PredictionOut)
def get_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(database.Prediction).filter(database.Prediction.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record
