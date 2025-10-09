from fastapi import FastAPI
from .routes import notifications

app = FastAPI(title="Notifications Service")

app.include_router(notifications.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "notifications-service"}
