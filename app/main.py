from demo_data import lead_data_values, degree_data_values, signature_data_values, pdb_data_values, pbs_data_values
import requests
import json
from typing import List

from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

# Change to True if you want to fill database with some data
demo = True

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Demo Data
@app.post("/demo-data/")
def demo_data():
    root = 'http://127.0.0.1:8000/'
    if demo:
        for data in lead_data_values:
            url = root + 'leads/'
            requests.post(url, data=json.dumps(data))
        for data in degree_data_values:
            url = root + 'degree/'
            requests.post(url, data=json.dumps(data))
        for data in signature_data_values:
            url = root + 'signature/'
            requests.post(url, data=json.dumps(data))
        for data in pdb_data_values:
            url = root + 'pbd/'
            requests.post(url, data=json.dumps(data))
        for data in pbs_data_values:
            url = root + 'pbs/'
            requests.post(url, data=json.dumps(data))
        return HTTPException(status_code=200, detail="Demo was finally installed")
    else:
        raise HTTPException(status_code=400, detail="Demo is not available")


# Leads Section
@app.post("/leads/", response_model=schemas.Lead)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    if crud.get_lead_by_email(db, email=lead.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if crud.get_lead_by_dni(db, dni=lead.dni):
        raise HTTPException(status_code=400, detail="DNI already registered")
    return crud.create_lead(db=db, lead=lead)


@app.get("/leads/", response_model=List[schemas.Lead])
def read_leads(skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    leads = crud.get_leads(db, skip=skip, limit=limit)
    return leads


@app.get("/leads/{lead_id}", response_model=schemas.Lead)
def read_lead(lead_id: int, db: Session = Depends(get_db)):
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
    signature.time_signature = signature.monthly_duration * 4 * signature.weekly_hours
    return crud.create_signature(db=db, signature=signature)


# Projection By Degree Section
@app.post("/pbd/", response_model=schemas.ProjectionByDegree)
def create_pbd(pbd: schemas.ProjectionByDegreeCreate, db: Session = Depends(get_db)):
    return crud.create_projections_by_degree(db=db, pbd=pbd)


# Projection By Signature Section
@app.post("/pbs/", response_model=schemas.ProjectionBySignature)
def create_pbs(pbs: schemas.ProjectionBySignatureCreate, db: Session = Depends(get_db)):
    return crud.create_projections_by_signature(db=db, pbs=pbs)


@app.put("/calculate-time/{lead_id}", response_model=schemas.Lead)
def calculate_total_cursing_hours(lead_id: int, db: Session = Depends(get_db)):
    lead = crud.get_lead(db, lead_id)
    total_cursing_hours = 0
    for projection_degree in lead.projection_by_degree:
        pbd_time = 0
        for projection_signature in projection_degree.projections_by_signature:
            projection_signature.pbs_time = projection_signature.signature.time_signature * projection_signature.times
            pbd_time += projection_signature.pbs_time
        projection_degree.pbd_time = pbd_time
        total_cursing_hours += projection_degree.pbd_time
    lead.total_cursing_hours = total_cursing_hours
    return lead
