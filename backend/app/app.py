#Libraries Import
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import webbrowser

#Services Import
from app.db import Base, engine
from app.routes.test_routes import test
from app.routes.employee import employee
from app.auth import auth


Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(auth)
app.include_router(test)
app.include_router(employee)

# Serve frontend — mount AFTER your API routes
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

@app.on_event("startup")
async def open_browser():
    webbrowser.open("http://localhost:8000/pages/index.html")




