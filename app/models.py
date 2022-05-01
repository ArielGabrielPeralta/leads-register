from sqlalchemy import Column, ForeignKey, Integer, String, Table, Date
from sqlalchemy.orm import relationship

from .database import Base


class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), index=True)
    surname = Column(String(32), index=True)
    address = Column(String(110))
    email = Column(String)
    dni = Column(Integer)
    phone = Column(Integer)
    inscription = Column(Date)
    total_cursing_hours = Column(Integer)

    projection_by_degree = relationship("ProjectionByDegree", back_populates='lead')


class BachelorsDegree(Base):
    __tablename__ = "bachelors_degrees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(48), index=True)

    projections_by_degree = relationship("ProjectionByDegree", back_populates='bachelors_degrees')


class Signature(Base):
    __tablename__ = "signatures"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(48), index=True)
    monthly_duration = Column(Integer, default=4)
    weekly_hours = Column(Integer)
    time_signature = Column(Integer)

    projections_by_signature = relationship("ProjectionBySignature", back_populates='signature')


class ProjectionByDegree(Base):
    __tablename__ = "projections_by_degree"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey('leads.id'))
    bachelors_degrees_id = Column(Integer, ForeignKey('bachelors_degrees.id'))
    pbd_time = Column(Integer)

    projections_by_signature = relationship("ProjectionBySignature", back_populates='projections_by_degree')
    bachelors_degrees = relationship("BachelorsDegree", back_populates='projections_by_degree')
    lead = relationship("Lead", back_populates='projection_by_degree')


class ProjectionBySignature(Base):
    __tablename__ = "projections_by_signature"
    id = Column(Integer, primary_key=True, index=True)
    times = Column(Integer, default=0)
    signature_id = Column(Integer, ForeignKey('signatures.id'))
    projections_by_degree_id = Column(Integer, ForeignKey('projections_by_degree.id'))
    pbs_time = Column(Integer)

    signature = relationship("Signature", back_populates='projections_by_signature')
    projections_by_degree = relationship("ProjectionByDegree", back_populates='projections_by_signature')
