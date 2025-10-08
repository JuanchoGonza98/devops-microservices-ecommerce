from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/orders", tags=["Orders"])

PRODUCT_SERVICE_URL = "http://product-service:8081"  # nombre del servicio en docker-compose

ORDERS = []
ORDER_ID_COUNTER = 1

@router.post("/")
def create_order(order_data: dict):
    global ORDER_ID_COUNTER

    total = 0
    detailed_products = []

    # recorrer los productos enviados en el pedido
    for item in order_data["products"]:
        # llamada al product-service
        try:
            response = httpx.get(f"{PRODUCT_SERVICE_URL}/products/{item['id']}")
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

    new_order = {
        "id": ORDER_ID_COUNTER,
        "user_id": order_data["user_id"],
        "products": detailed_products,
        "total": total,
        "status": "pending"
    }

    ORDERS.append(new_order)
    ORDER_ID_COUNTER += 1

    return new_order
