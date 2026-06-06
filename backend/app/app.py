from fastapi import FastAPI, HTTPException
from datetime import datetime
from app.utils import validate_ph, hash_password, generate_emp_id, write_json, verify_password, database
from app.schemas import SignupSchema, LoginSchema
from app.routes.test_routes import test
from app.routes.auth import auth

app=FastAPI()

app.include_router(auth)
app.include_router(test)