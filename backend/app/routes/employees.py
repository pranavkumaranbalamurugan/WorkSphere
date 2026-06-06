"""from fastapi import APIRouter, HTTPException
from app.schemas import CreateEmployeeSchema

employee=(APIRouter)

@employee.post("/api/employees")
def create_employee(employee: CreateEmployeeSchema):
    """
