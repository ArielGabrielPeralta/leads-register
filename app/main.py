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


# Leads Section
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


# Degree Section
@app.post("/degree/", response_model=schemas.BachelorsDegree)
def create_degree(degree: schemas.BachelorsDegreeCreate, db: Session = Depends(get_db)):
    db_degree = crud.get_bachelors_degree_by_name(db, bachelors_degree_name=degree.name)
    if db_degree:
        raise HTTPException(status_code=400, detail="Bachelor's Degree already exist")
    return crud.create_bachelors_degree(db=db, bachelors_degree=degree)


# Signature Section
@app.post("/signature/", response_model=schemas.Signature)
def create_signature(signature: schemas.SignatureCreate, db: Session = Depends(get_db)):
    db_signature = crud.get_signature_by_name(db, signature_name=signature.name)
    if db_signature:
        raise HTTPException(status_code=400, detail="Signature already exist")
    return crud.create_signature(db=db, signature=signature)


# Projection By Degree Section
@app.post("/pbd/", response_model=schemas.ProjectionByDegree)
def create_pbd(pbd: schemas.ProjectionByDegreeCreate, db: Session = Depends(get_db)):
    return crud.create_projections_by_degree(db=db, pbd=pbd)


# Projection By Signature Section
@app.post("/pbs/", response_model=schemas.ProjectionBySignature)
def create_pbs(pbs: schemas.ProjectionBySignatureCreate, db: Session = Depends(get_db)):
    return crud.create_projections_by_signature(db=db, pbs=pbs)
