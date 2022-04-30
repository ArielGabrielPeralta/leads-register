from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from .database import Base

association_table = Table('association', Base.metadata,
                          Column('bachelors_degrees_id', ForeignKey('bachelors_degrees_id.id'), primary_key=True),
                          Column('signatures_', ForeignKey('signatures.id'), primary_key=True)
                          )


class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), index=True)
    surname = Column(String(32), index=True)
    address = Column(String(110))
    email = relationship("Email", back_populates="lead", uselist=False)
    phone = Column(Integer)
    projections_by_degree = relationship("ProjectionByDegree", back_populates="lead")


class BachelorsDegree(Base):
    __tablename__ = "bachelors_degrees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(48), index=True)
    signatures = relationship("Signature", back_populates="bachelors_degree", secondary=association_table)


class Signature(Base):
    __tablename__ = "signatures"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(48), index=True)
    duration = Column(Integer, default=4)
    bachelors_degree = relationship("BachelorsDegree", back_populates="signatures", secondary=association_table)


class ProjectionByDegree(Base):
    __tablename__ = "projections_by_degree"
    id = Column(Integer, primary_key=True, index=True)
    lead = relationship("Lead", back_populates="projections_by_degree")
    bachelors_degree = relationship("BachelorsDegree")
    projections_by_signature = relationship("ProjectionBySignature")


class ProjectionBySignature(Base):
    __tablename__ = "projections_by_signature"
    id = Column(Integer, primary_key=True, index=True)
    bachelors_degree = relationship("BachelorsDegree")
    signature = relationship("Signature")
    times = Column(Integer, default=0)


class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    lead_id = Column(Integer, ForeignKey('lead.id'))
    lead = relationship("Lead", back_populates="email")

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("failed simple email validation")
        return email
