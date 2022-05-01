from datetime import date

from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class SignatureBase(BaseModel):
    name: str
    monthly_duration: int = 4
    weekly_hours: int = Field(..., gt=0, lt=50)


class Signature(SignatureBase):
    id: int
    time_signature: int = 0

    class Config:
        orm_mode = True


class SignatureCreate(SignatureBase):
    time_signature: int = 0


class BachelorsDegreeBase(BaseModel):
    name: str


class BachelorsDegree(BachelorsDegreeBase):
    id: int

    class Config:
        orm_mode = True


class BachelorsDegreeCreate(BachelorsDegreeBase):
    pass


class ProjectionBySignatureBase(BaseModel):
    times: int = 0


class ProjectionBySignature(ProjectionBySignatureBase):
    id: int
    signature: Signature = None
    pbs_time: int = 0

    class Config:
        orm_mode = True


class ProjectionBySignatureCreate(ProjectionBySignatureBase):
    projections_by_degree_id: int
    signature_id: int
    pbs_time: Optional[int] = 0


class ProjectionByDegreeBase(BaseModel):
    pass


class ProjectionByDegree(ProjectionByDegreeBase):
    id: int
    bachelors_degrees: BachelorsDegree
    projections_by_signature: List[ProjectionBySignature]
    pbd_time: Optional[int] = 0

    class Config:
        orm_mode = True


class ProjectionByDegreeCreate(ProjectionByDegreeBase):
    lead_id: int
    bachelors_degrees_id: int
    pbd_time: Optional[int] = 0


class LeadBase(BaseModel):
    name: str
    surname: str
    address: str
    email: EmailStr
    dni: int = Field(..., gt=0, le=99999999)
    phone: int = Field(..., gt=0, le=9999999999)
    inscription: date


class Lead(LeadBase):
    id: int
    projection_by_degree: List[ProjectionByDegree]
    total_cursing_hours: int = 0

    class Config:
        orm_mode = True


class LeadCreate(LeadBase):
    total_cursing_hours: Optional[int] = 0
