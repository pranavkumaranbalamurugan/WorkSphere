#Libraries Import
from fastapi import APIRouter,HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

#Services Import
from app.utils import  generate_emp_id, require_roles, generate_work_email, fetch_company_details, validate_ph, format_phone
from app.schemas import CreateEmployeeSchema, UpdateEmployeeSchema,TokenData
from app.db import get_db
from app.models import Employee, User
from app.config import bcrypt_context

employee=APIRouter(tags=["employee"])

@employee.post("/api/employee")
def create_employee(
    employee:CreateEmployeeSchema, 
    db: Session=Depends(get_db), 
    current_user:TokenData=Depends(require_roles(["ADMIN", "HR"])) 
):
    
    company=fetch_company_details (current_user["company_id"],db)

    id=generate_emp_id(db)
    mail=generate_work_email(employee.first_name, employee.last_name, current_user["company_id"],db) 
    temp_pwd=bcrypt_context.hash(id)


    new_employee = Employee(
        emp_id=id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        work_email=mail,
        manager=employee.manager,
        company_name=company["name"],
        joining_date=datetime.now().date()
    )

    new_user = User(
        work_email=mail,
        hashed_password=temp_pwd,
        role="Employee",
        company_id=company["id"]
    )
    
    try:

        db.add(new_employee)
        db.add(new_user)
        db.commit()
        db.refresh(new_employee)
        db.refresh(new_user)

        return {"message": "employee created successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e) )
        


@employee.get("/api/employees")
def get_all_employees(
    current_user:TokenData=Depends(require_roles(["ADMIN", "HR"])),
    db:Session=Depends(get_db)
):

    company=fetch_company_details (current_user["company_id"],db)
    
    return (
        db.query(Employee)
        .filter(Employee.company_name.like(company["name"]))
        .all()
    )

@employee.get("/api/employees/{emp_id}")
def get_employee(emp_id:str,
    current_user:TokenData=Depends(require_roles(["ADMIN","HR"])),
    db:Session=Depends(get_db)
):

    company=fetch_company_details (current_user["company_id"],db)

    return  (
        db.query(Employee)
        .filter(Employee.company_name.like(company["name"]))
        .filter(Employee.emp_id.like(emp_id))
        .first()
    )

@employee.put("/api/employees/{emp_id}")
def update_employee(
     employee:UpdateEmployeeSchema,
    emp_id:str,
    current_user:TokenData=Depends(require_roles(["ADMIN", "HR"])),
    db:Session=Depends(get_db)
):
    
    if not validate_ph(employee.phone):
        return HTTPException(status_code=400,detail="Invalid Phone number")
    
    ph=format_phone(employee.country, employee.phone)
     
    new_employee_data = Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        personal_email=employee.personal_email,
        phone=ph
    )
    
    return {"message":"employee created successfully"}

@employee.delete("/api/employees/{emp_id}")
def delete(
    emp_id:str,
    current_user:TokenData=Depends(require_roles(["ADMIN", "HR"])),
    db: Session=Depends(get_db)
):
    
        deleted_employee = db.query(Employee).filter(Employee.emp_id.like( emp_id)).first()
        if not deleted_employee:
            raise HTTPException(status_code=404, detail="Employee ID not found!")

        db.delete(deleted_employee)
        db.commit()

        return {
            "message": "employee deleted",
            "deleted_data": deleted_employee
            }

