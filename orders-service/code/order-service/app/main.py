from fastapi import FastAPI
from app.routes import orders

app = FastAPI(
    title="Orders Service",
    version="1.0.0",
    description="Microservicio responsable de la gestión de pedidos."
)

app.include_router(orders.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "orders-service"}
