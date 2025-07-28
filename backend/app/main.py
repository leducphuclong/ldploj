from fastapi import FastAPI
from .api.v1.api import api_router

app = FastAPI(title="LDPL OJ Production API (PostgreSQL + Alembic)"
             , version="1.0.0"
             , description="This is the production API for LDPL OJ, built with FastAPI, PostgreSQL, and Alembic for migrations.")

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "ok", "message": "API is running"}