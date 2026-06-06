from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import date

class Test_Signup(BaseModel):

    first_name: str
    last_name: str
    email: EmailStr
    password: str
    confirm_password: str
    phone: str
    role: str

class LoginSchema(BaseModel):
    
    email: EmailStr
    password: str

class CreateEmployeeSchema(BaseModel):

    first_name: str
    work_email:EmailStr
    department: str
    role: str
    manager: str
    joining_date: date
    temp_password: str
