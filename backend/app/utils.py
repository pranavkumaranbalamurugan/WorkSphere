#Libraries Import
import bcrypt
from fastapi import Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Annotated
from jose import jwt, JWTError
from starlette import status

#Services Import
from app.models import Employee, Companies, User
from app.schemas import TokenData
from app.db import get_db
from app.config import SECRET_KEY, ALGORITHM, oauth2_scheme

#Employee ID generation
def generate_emp_id(db: Session):

    current_year = datetime.now().year

    # Get latest employee of current year
    latest_employee = (
        db.query(Employee)
        .filter(Employee.emp_id.like(f"EMP{current_year}%"))
        .order_by(Employee.emp_id.desc())
        .first()
    )

    # First employee of the year
    if not latest_employee:

        return f"EMP{current_year}0001"

    # Extract last 4 digits
    last_number = int(latest_employee.emp_id[-4:])

    new_number = last_number + 1

    formatted_number = str(new_number).zfill(4)

    return f"EMP{current_year}{formatted_number}"


#Validations
def validate_ph(phone: str):
    return phone.isdigit() and len(phone) == 10


#RBAC Models

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        work_email = payload.get("work_email")
        role = payload.get("role")
        company_id=payload.get("company_id")

        if work_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication"
            )

        return {
            "work_email":work_email,
            "role": role,
            "company_id": company_id
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
user_dependency = Annotated[dict, Depends(get_current_user)]
    
def require_role(allowed_roles: list):

    def role_checker(user: user_dependency):

        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Operation not permitted"
            )

        return user

    return role_checker


def require_roles(allowed_roles: list[str]):

    def checker(
        current_user: Annotated[
            TokenData,
            Depends(get_current_user)
        ]
    ):

        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

        return current_user

    return checker


def generate_work_email(first_name:str, last_name:str, company_id:int, db:Session = Depends(get_db)):

    company_details= fetch_company_details(company_id,db)
    company_domain=company_details["domain"]

    first_name=first_name.lower()
    last_name=last_name.lower()

    return f"{first_name}.{last_name}@{company_domain}"

def format_phone(country:str,phone:str):
    
    country_codes={"India":"+91"}

    code=country_codes[country]
    
    if code is None:
        raise ValueError(f"Unsupported Country: {country}")

    
    first=phone[0:5]
    last=phone[5:]

    return f"{code} {first} {last}"

def fetch_company_details(company_id: int, db: Session):
    company = (
        db.query(Companies)
        .filter(Companies.company_id == company_id)
        .first()
    )

    return {
        "id": company.company_id,
        "name": company.company_name,
        "domain": company.company_domain
    }
def get_company_details(
    current_user: Annotated[TokenData, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    return fetch_company_details(current_user.company_id, db)