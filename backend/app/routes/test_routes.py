from fastapi import APIRouter,HTTPException
from app.utils import validate_ph, hash_password, generate_emp_id, write_json, verify_password, database
from app.schemas import Test_Signup, LoginSchema

test=APIRouter()

@test.post("/api/test/signup")
def signup(user: Test_Signup):

    if not validate_ph(user.phone):
        raise HTTPException(status_code=422, detail="invalid number")
    
    elif user.password!=user.confirm_password:
        raise HTTPException(status_code=400, detail="passwords do not match")
    
    
    for emp in database.values():
            if emp["email"] == user.email:
                raise HTTPException(status_code=400, detail="email already exists")
            
    emp_id=generate_emp_id()
    password=hash_password(user.password)
     
    database[emp_id]={
        "first_name": user.first_name,
        "last_name": user.last_name, 
        "email": user.email,
        "password": password,
        "phone": user.phone, 
        "role": user.role
        }
                
    write_json("database", database)

    return {"message":"Signed up successfully"}

@test.delete("/api/test/delete_all_values")
def delete_all_values(secret: str):
    
    global database

    if secret == "PRANAV":
        
        database = {}

        write_json("database", database)

        return {"message": "all data deleted"}

    return {"message": "invalid secret"}

@test.delete("/api/test/delete/{emp_id}")
def delete(emp_id:str):
    
    global database
    
    if emp_id not in database:
        raise HTTPException(status_code=404, detail="Employee ID not found! ")
    else:
        deleted_employee = database.pop(emp_id)

        write_json("database", database)

        return {
            "message": "employee deleted",
            "deleted_data": deleted_employee
            }
