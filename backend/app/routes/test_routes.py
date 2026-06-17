#Libraries Import
from fastapi import APIRouter , HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends

#Services Import
from app.models import Employee, Companies, User
from app.schemas import CompanySignupSchema
from app.db import get_db

test=APIRouter(tags=["test"])


@test.delete("/api/test/delete_all_employees")
def delete_all_values(secret: str, db: Session=Depends(get_db)):


    if secret == "PRANAV":
        
        num_deleted = db.query(Employee).delete()
        db.commit()
        
        return {"message": "all data deleted"}

    return {"message": "invalid secret"}

@test.post ("/api/test/create_company")
def create_company(company: CompanySignupSchema,db:Session=Depends(get_db)):

    new_company = Companies(
        company_name=company.company_name,
        company_domain=company.company_domain
    )

    try:
        db.add(new_company)
        db.commit()
        db.refresh(new_company)

        company_id=(
            db.query(Companies.company_id)
            .filter(Companies.company_name.like(company.company_name))
            .scalar()    
        )

        return {
            "messgae": "company added successfully",
            "comapany_id": company_id 
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code =500, detail=str(e))
    
@test.get("/api/test/users")
def get_users(db:Session=Depends(get_db)):

    return db.query(User).all()
