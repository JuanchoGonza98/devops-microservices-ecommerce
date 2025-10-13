from fastapi import APIRouter, HTTPException
import httpx, os

router = APIRouter(prefix="/orders", tags=["Orders"])

# URLs internas definidas en docker-compose
PRODUCTS_API_URL = os.getenv("PRODUCTS_API_URL", "http://products-service:8081")
USERS_API_URL = os.getenv("USERS_API_URL", "http://users-service:8084")
PAYMENTS_API_URL = os.getenv("PAYMENTS_API_URL", "http://payments-service:8082")

ORDERS = []
ORDER_ID_COUNTER = 1


@router.post("/")
def create_order(order_data: dict):
    global ORDER_ID_COUNTER

    # ✅ 1. Validar usuario
    user_id = order_data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id")

    try:
        user_resp = httpx.get(f"{USERS_API_URL}/users/{user_id}")
        if user_resp.status_code == 404:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        elif user_resp.status_code != 200:
            raise HTTPException(status_code=500, detail="Error validating user")
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="Error connecting to users-service")

    # ✅ 2. Validar productos
    total = 0
    detailed_products = []

    for item in order_data["products"]:
        try:
            response = httpx.get(f"{PRODUCTS_API_URL}/products/{item['id']}")
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail=f"Product {item['id']} not found")

            product = response.json()
            subtotal = product["price"] * item["quantity"]
            total += subtotal

            detailed_products.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": item["quantity"],
                "subtotal": subtotal
            })
        except httpx.RequestError:
            raise HTTPException(status_code=500, detail="Error connecting to product-service")

    # ✅ 3. Crear orden local
    new_order = {
        "id": ORDER_ID_COUNTER,
        "user_id": user_id,
        "products": detailed_products,
        "total": total,
        "status": "pending"
    }
    ORDERS.append(new_order)
    ORDER_ID_COUNTER += 1

    # ✅ 4. Llamar al payments-service
    try:
        payment_resp = httpx.post(f"{PAYMENTS_API_URL}/payments/{new_order['id']}")
        if payment_resp.status_code != 200:
            raise HTTPException(status_code=payment_resp.status_code, detail="Payment processing failed")

        payment_data = payment_resp.json()
        new_order["status"] = "paid"
        new_order["payment"] = payment_data
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="Error connecting to payments-service")

    # ✅ 5. Devolver respuesta final
    return {
        "order_id": new_order["id"],
        "status": "PAID",
        "total": total,
        "message": "Order processed successfully"
    }
