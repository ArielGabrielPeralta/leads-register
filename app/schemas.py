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


class BachelorsDegreeBase(BaseModel):
    name: str


class BachelorsDegree(BachelorsDegreeBase):
    id: int
    signatures: List[Signature]

    class Config:
        orm_mode = True


class ProjectionBySignatureBase(BaseModel):
    times: int = 0


class ProjectionBySignature(ProjectionBySignatureBase):
    id: int
    bachelors_degree: int
    signature: int

    class Config:
        orm_mode = True


class ProjectionByDegreeBase(BaseModel):
    pass


class ProjectionByDegree(ProjectionByDegreeBase):
    id: int
    lead: int
    bachelors_degree: int
    projections_by_signature: List[ProjectionBySignature]

    class Config:
        orm_mode = True


class StudentBase(BaseModel):
    name: str
    surname: str
    address: str
    email: EmailStr
    phone: int
    inscription: date


class Student(StudentBase):
    id: int
    projections_by_degree: List[ProjectionByDegree]

    class Config:
        orm_mode = True
