#Libraries Import
from sqlalchemy import Column, Integer, String, DateTime

#Services Import
from app.db import Base

class Employee(Base):
    __tablename__="employees"

    emp_id=Column(String, primary_key=True, index=True)
    first_name= Column(String)
    last_name= Column(String)
    personal_email=Column(String, unique=True)
    work_email=Column(String, unique=True)
    phone=Column(String, unique=True) 
    hashed_password=Column(String)
    role=Column(String)
    manager=Column(String)
    company_name=Column(String)
    joining_date=Column(DateTime)

class Companies(Base):
    __tablename__="companies"

    company_id=Column(Integer, primary_key=True, autoincrement=True)
    company_name=Column(String)
    company_domain=Column(String)
    admin_email=Column(String)

class User(Base):
    __tablename__="users"

    work_email=Column(String, primary_key=True)
    hashed_password=Column(String)
    role=Column(String)
    company_id=Column(Integer)