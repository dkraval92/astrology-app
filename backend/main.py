from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import database, models, astrology

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Astrology API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    full_name: str
    dob: str
    tob: str
    place: str
    email: str
    mobile: str
    gender: str = "Other"

@app.post("/api/kundli/generate")
def generate_kundli(data: UserInput, db: Session = Depends(database.get_db)):
    lat, lon = astrology.get_lat_lon(data.place)
    chart_data = astrology.calculate_chart(data.dob, data.tob, lat, lon)
    
    record = models.KundliRecord(
        full_name=data.full_name, dob=data.dob, tob=data.tob,
        place=data.place, email=data.email, mobile=data.mobile,
        gender=data.gender, latitude=lat, longitude=lon,
        ascendant_sign=chart_data["ascendant_sign"]
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    
    predictions = [{"category": "Personality", "text": f"Your {chart_data['ascendant_name']} ascendant gives you a unique approach to life."}]
        
    return {
        "id": record.id,
        "user_info": data,
        "chart_data": chart_data,
        "predictions": predictions
    }
