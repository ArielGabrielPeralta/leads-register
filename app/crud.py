from sqlalchemy.orm import Session

from . import models, schemas


def get_lead(db: Session, lead_id: int):
    return db.query(models.Lead).filter(models.Lead.id == lead_id).first()


def get_lead_by_email(db: Session, email: str):
    return db.query(models.Lead).filter(models.Lead.email == email).first()


def get_lead_by_dni(db: Session, dni: int):
    return db.query(models.Lead).filter(models.Lead.dni == dni).first()


def get_leads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lead).offset(skip).limit(limit).all()


def create_bachelors_degree(db: Session, bachelors_degree: schemas.BachelorsDegreeCreate):
    db_bachelors_degree = models.BachelorsDegree(name=bachelors_degree.name)
    db.add(db_bachelors_degree)
    db.commit()
    db.refresh(db_bachelors_degree)
    return db_bachelors_degree


def get_bachelors_degree_by_name(db: Session, bachelors_degree_name: str):
    return db.query(models.BachelorsDegree).filter(models.BachelorsDegree.name == bachelors_degree_name).first()


def create_signature(db: Session, signature: schemas.SignatureCreate):
    db_signature = models.Signature(**signature.dict())
    db.add(db_signature)
    db.commit()
    db.refresh(db_signature)
    return db_signature


def get_signature_by_name(db: Session, signature_name: str):
    return db.query(models.Signature).filter(models.Signature.name == signature_name).first()


def create_lead(db: Session, lead: schemas.LeadCreate):
    db_lead = models.Lead(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead


def create_projections_by_degree(db: Session, pbd: schemas.ProjectionByDegreeCreate):
    # projections_by_degree as pbd
    db_pbd = models.ProjectionByDegree(**pbd.dict())
    db.add(db_pbd)
    db.commit()
    db.refresh(db_pbd)
    return db_pbd


def create_projections_by_signature(db: Session, pbs: schemas.ProjectionBySignatureCreate):
    # projections_by_signature as pbs
    db_pbs = models.ProjectionBySignature(**pbs.dict())
    db.add(db_pbs)
    db.commit()
    db.refresh(db_pbs)
    return db_pbs
