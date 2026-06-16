#Libraries Import
from fastapi import APIRouter,HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

#Services Import
from app.utils import  generate_emp_id, require_roles, generate_work_email, get_company_details
from app.schemas import CreateEmployeeSchema, TokenData
from app.db import get_db
from app.models import Employee
from app.config import bcrypt_context

employee=APIRouter()

@employee.post("/api/employee")
def create_employee(
     employee:CreateEmployeeSchema, 
    db: Session=Depends(get_db), 
    current_user:TokenData=Depends(require_roles(["ADMIN", "HR"])) ):
    
    id=generate_emp_id(db)
    mail=generate_work_email(employee.first_name, employee.last_name)
    temp_pwd=bcrypt_context.hash(id)


    new_employee = Employee(
        emp_id=id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        work_email=mail,
        hashed_password=temp_pwd,
        role="Employee",
        manager=employee.manager,
        company_name=company.name,
        joining_date=datetime.now().date,  
    )
    
    try:

        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)

        return {"message": "employee added successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e) )
        


@employee.get("/api/employees")
def get_all_employees(db:Session=Depends(get_db)):
   
    return db.query(Employee).filter(Employee.company_name.like(company.name))


@employee.delete("/api/employee/{emp_id}")
def delete(emp_id:str, db: Session=Depends(get_db)):
    
        deleted_employee = db.query(Employee).filter(Employee.emp_id == emp_id).first()
        if not deleted_employee:
            raise HTTPException(status_code=404, detail="Employee ID not found!")

        db.delete(deleted_employee)
        db.commit()

        return {
            "message": "employee deleted",
            "deleted_data": deleted_employee
            }