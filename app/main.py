from fastapi import FastAPI
from app.routes import animal_routes

app = FastAPI(title="Wildlife AI API")

app.include_router(animal_routes.router, prefix="/api")