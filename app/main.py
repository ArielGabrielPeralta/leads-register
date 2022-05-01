from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/leads/", response_model=schemas.Lead)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    db_lead = crud.get_lead_by_email(db, email=lead.email)
    if db_lead:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_lead(db=db, lead=lead)


@app.get("/leads/", response_model=List[schemas.Lead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    leads = crud.get_leads(db, skip=skip, limit=limit)
    return leads


@app.get("/leads/{lead_id}", response_model=schemas.Lead)
def read_user(lead_id: int, db: Session = Depends(get_db)):
    db_lead = crud.get_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead
