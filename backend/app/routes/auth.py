from fastapi import APIRouter, HTTPException
from app.utils import verify_password, database
from app.schemas import LoginSchema

auth=APIRouter()

@auth.post("/api/auth/login")
def login(user:LoginSchema):
    for emp in database.values():
        
        if emp["email"]==user.email:
            
            password=emp["password"]
            break
        
        else:
            
            raise HTTPException(status_code=404,detail="email does not exist")

    if verify_password(user.password,password)==False:
        
        raise HTTPException(status_code=401, detail="Invalid Email or Password")
    
    else:
        
        return {"message": "Login Successfull"}
