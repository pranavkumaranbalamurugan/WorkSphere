#Libraries Import
from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import date

class CreateUserRequest(BaseModel):
    work_email:EmailStr
    password:str
    role:str
    company_id:int

class CreateUser(BaseModel):
    emp_id: str
    first_name: str
    last_name: str
    personal_email: EmailStr
    work_email: EmailStr
    phone: str
    department: str
    hashed_password: str
    role: str
    department: str
    manager: str
    designation: str
    joining_date:date
    hashed_password: str

class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    emp_id:str
    role:str
    company_id:str

class CreateEmployeeSchema(BaseModel):

    first_name: str
    last_name:str
    manager: str

class CompanySignupSchema(BaseModel):
    company_name:str
    company_domain:str

class AdminSignupSchema(BaseModel):
    first_name:str
    last_name:str
    personal_email:EmailStr
    work_email:EmailStr
    hashed_password:str
    confirm_password:str
    
