from datetime import date

from typing import List, Optional

from pydantic import BaseModel, EmailStr


class SignatureBase(BaseModel):
    name: str
    duration: Optional[int] = 4


class Signature(SignatureBase):
    id: int

    class Config:
        orm_mode = True


class SignatureCreate(SignatureBase):
    pass


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

    class Config:
        orm_mode = True


class ProjectionBySignatureCreate(ProjectionBySignatureBase):
    projections_by_degree_id: int
    signature_id: int


class ProjectionByDegreeBase(BaseModel):
    pass


class ProjectionByDegree(ProjectionByDegreeBase):
    id: int
    bachelors_degrees: BachelorsDegree
    projections_by_signature: List[ProjectionBySignature]

    class Config:
        orm_mode = True


class ProjectionByDegreeCreate(ProjectionByDegreeBase):
    lead_id: int
    bachelors_degrees_id: int


class LeadBase(BaseModel):
    name: str
    surname: str
    address: str
    email: EmailStr
    phone: int
    inscription: date


class Lead(LeadBase):
    id: int
    projections_by_degree: List[ProjectionByDegree]

    class Config:
        orm_mode = True


class LeadCreate(LeadBase):
    pass
