from fastapi import FastAPI
from app.api.endpoints import incidents, authentication

app = FastAPI(title="Incident Management System")

app.include_router(incidents.router, prefix="/incidents", tags=["Incidents"])
app.include_router(authentication.router, prefix="/auth", tags=["Auth"])