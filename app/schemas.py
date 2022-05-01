from datetime import date

from typing import List, Optional

from pydantic import BaseModel, EmailStr


class SignatureBase(BaseModel):
    name: str
    duration: Optional[int] = 4


class Signature(SignatureBase):
    id: int
    bachelors_degree_id: int

    class Config:
        orm_mode = True


class SignatureCreate(SignatureBase):
    pass


class BachelorsDegreeBase(BaseModel):
    name: str


class BachelorsDegree(BachelorsDegreeBase):
    id: int
    signatures: List[Signature]

    class Config:
        orm_mode = True


class BachelorsDegreeCreate(BachelorsDegreeBase):
    pass


class ProjectionBySignatureBase(BaseModel):
    times: int = 0


class ProjectionBySignature(ProjectionBySignatureBase):
    id: int
    bachelors_degree: int
    signature: int

    class Config:
        orm_mode = True


class ProjectionBySignatureCreate(ProjectionBySignatureBase):
    pass


class ProjectionByDegreeBase(BaseModel):
    lead: int


class ProjectionByDegree(ProjectionByDegreeBase):
    id: int
    bachelors_degree: int
    projections_by_signature: List[ProjectionBySignature]

    class Config:
        orm_mode = True


class ProjectionByDegreeCreate(ProjectionByDegreeBase):
    pass


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
