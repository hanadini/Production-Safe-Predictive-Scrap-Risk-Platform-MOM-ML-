from fastapi import FastAPI
from MLService.api.routes import router

app = FastAPI(
    title="Production-Safe Predictive Scrap Risk Platform",
    description="FastAPI service for production-safe scrap risk prediction in MOM/MES environments",
    version="1.0.0"
)

app.include_router(router)