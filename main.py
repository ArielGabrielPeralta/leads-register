from datetime import date

from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Signature(BaseModel):
    name: str
    duration: Optional[int] = 4


class BachelorsDegree(BaseModel):
    name: str
    signatures: Optional[List[Signature]] = []


class Student(BaseModel):
    name: str
    surname: str
    email: Optional[EmailStr]
    address: str
    phone: int
    bachelors_degree: List[BachelorsDegree]
    inscription: date


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/student/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
