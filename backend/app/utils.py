import bcrypt
from datetime import datetime
import json


#Employee ID generation
def generate_emp_id():
    
    year = datetime.now().year
    emp_count=employee_count()
    formatted_id = str(emp_count).zfill(4)
    emp_id = f"EMP{year}{formatted_id}"

    return emp_id

def employee_count():
    
    current_year = str(datetime.now().year)
    
    if not database:
        return 1
    
    else:
        
        last_emp_id=list(database.keys())[-1]
        last_year=last_emp_id[3:7]

        if last_year==current_year:
            
            last_number = int(last_emp_id[-4:])
            return last_number + 1
        
        else:
            return 1


#Password Hashing
def hash_password(password: str):

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw( password.encode("utf-8"), salt)

    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str):

    return bcrypt.checkpw( plain_password.encode("utf-8"),hashed_password.encode("utf-8"))

#Validations
def validate_ph(phone: str):
    return phone.isdigit() and len(phone) == 10

#Database File Management
def read_json(filename: str,):
    
    with open("database/"+filename+".json", "r") as file:
        database = json.load(file)

        return database

database=read_json("database")

def write_json(filename: str, database: dict):

    with open("database/"+filename + ".json", "w") as file:
        json.dump(database, file, indent=4)
