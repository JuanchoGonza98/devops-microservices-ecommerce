from fastapi import FastAPI
from . import models, database
from .routes import users

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Users Service")

app.include_router(users.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "users-service"}
