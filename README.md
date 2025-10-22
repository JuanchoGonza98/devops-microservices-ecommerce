# 🛍️ E-Commerce Microservices – Proyecto DevOps Full Stack

Este proyecto es un **ecosistema de microservicios** que simula un sistema de e-commerce modularizado.  
Cada servicio está desarrollado con diferentes tecnologías (Java Spring Boot y Python FastAPI) y se comunican entre sí a través de **REST APIs**.  
El objetivo principal es aplicar conceptos de **DevOps, contenedorización, orquestación y arquitectura distribuida**.

---

## 🧩 Arquitectura General

| Componente | Tecnología | Descripción | Comunicación |
|-------------|-------------|--------------|---------------|
| **Frontend** | HTML + JavaScript | Interfaz de usuario que consume las APIs del gateway. | Envía solicitudes al `nginx-gateway`. |
| **API Gateway** | Nginx | Enruta las peticiones HTTP a los microservicios correctos. | Proxy hacia los microservicios backend. |
| **Products Service** | Java (Spring Boot) | Gestiona el catálogo de productos y stock. | Consumido por `orders-service` y `payments-service`. |
| **Orders Service** | Python (FastAPI) | Crea pedidos y coordina la interacción entre productos y pagos. | Invoca `products-service` y `payments-service`. |
| **Payments Service** | Java (Spring Boot) | Procesa los pagos y confirma transacciones además de mostrar mensaje de pagos. | Se comunica con `products-service` y `notifications-service`. |
| **Infraestructura** | Docker + Docker Compose | Orquestación y red interna entre servicios. | Red Docker `bridge` compartida. |

---



Los servicios se comunican internamente a través de una red Docker (`bridge`) y exponen sus APIs hacia el gateway Nginx.  
El gateway enruta el tráfico externo hacia el microservicio correspondiente.

---

## 🧱 Tecnologías Utilizadas

| Capa | Tecnología | Descripción |
|------|-------------|-------------|
| Backend (Java) | Spring Boot 3, Gradle, Java 17 | Servicios `products-service` y `payments-service` |
| Backend (Python) | FastAPI, Uvicorn | Servicios `orders-service` y `notifications-service` |
| Gateway | Nginx | Reverse proxy y enrutamiento de APIs |
| Contenerización | Docker, Docker Compose | Despliegue y comunicación entre servicios |
| Frontend | HTML, JavaScript | Cliente web que interactúa con el API Gateway |
| Orquestación (futuro) | Kubernetes / Tanzu | Escalabilidad y despliegue en clúster |

---

## 📂 Estructura del Proyecto

```bash
devops-microservices-ecommerce/
├── products-service/           # Java Spring Boot
├── payments-service/            # Java Spring Boot
├── orders-service/              # Python FastAPI
├── notifications-service/       # Python FastAPI
│
├── nginx-gateway/               # API Gateway (Nginx)
│   └── nginx.conf               # Configuración del enrutamiento
│
├── frontend/                    # Interfaz web (HTML + JS)
│   ├── index.html
│   └── app.js
│
├── docker-compose.yml           # Orquestación de contenedores
└── README.md                    # Documentación del proyecto


---

## ⚙️ Descripción de Microservicios

### 🧺 **Products Service (Java - Spring Boot)**
- Provee el catálogo de productos.
- Expone endpoints REST para listar, buscar y consultar stock.

### 💳 **Payments Service (Java - Spring Boot)**
- Procesa los pagos recibidos desde `orders-service`.
- Se comunica con `products-service` para verificar disponibilidad del producto.
- Notifica el estado del pago a `notifications-service` o al frontend.

### 📦 **Orders Service (Python - FastAPI)**
- Gestiona la creación de pedidos.
- Invoca `products-service` para verificar disponibilidad.
- Llama a `payments-service` para ejecutar el pago.

### 📧 **Notifications Service (Python - FastAPI)**
- Envía notificaciones (por ahora, simuladas via logs).
- Escucha peticiones desde `payments-service` u otros servicios.

---

## 🌐 **API Gateway (Nginx)**

El gateway enruta las solicitudes hacia el microservicio correspondiente:

```nginx
server {
    listen 80;

    location /products/ {
        proxy_pass http://products-service:8081/;
    }

    location /orders/ {
        proxy_pass http://orders-service:8083/;
    }

    location /payments/ {
        proxy_pass http://payments-service:8082/;
    }

    location /notifications/ {
        proxy_pass http://notifications-service:8000/;
    }
}
🖥️ Frontend

El frontend está implementado en HTML + JavaScript.
Se conecta al gateway para consumir los endpoints REST, por ejemplo:

fetch('http://localhost/api/orders', {
  method: 'POST',
  body: JSON.stringify(order),
  headers: { 'Content-Type': 'application/json' }
});
🐳 Despliegue con Docker Compose

Archivo docker-compose.yml:
version: "3.9"

services:
  # === PRODUCTS SERVICE ===
  products-service:
    image: juanchogonza98/e-commerce:product-servicev1.0.0
    container_name: products-service
    ports:
      - "8081:8081"
    environment:
      - SERVER_PORT=8081
    networks:
      - ecommerce-net
    restart: always

  # === USERS SERVICE ===
  users-service:
    image: juanchogonza98/e-commerce:users-servicelastest
    container_name: users-service
    ports:
      - "8084:8084"
    environment:
      - SERVER_PORT=8084
    networks:
      - ecommerce-net
    restart: always

  # === ORDERS SERVICE ===
  orders-service:
    image: juanchogonza98/e-commerce:order-servicefinal
    container_name: orders-service
    ports:
      - "8083:8083"
    environment:
      - SERVER_PORT=8083
      - PRODUCTS_API_URL=http://products-service:8081
      - USERS_API_URL=http://users-service:8084
    depends_on:
      - products-service
      - users-service
    networks:
      - ecommerce-net
    restart: always

  # === PAYMENTS SERVICE ===
  payments-service:
    image: juanchogonza98/e-commerce:payment-servicefinish
    container_name: payments-service
    ports:
      - "8082:8082"
    environment:
      - SERVER_PORT=8082
      - ORDERS_API_URL=http://orders-service:8083
    depends_on:
      - orders-service
    networks:
      - ecommerce-net
    restart: always

  # === FRONTEND (React + Nginx) ===
  frontend:
    image: juanchogonza98/e-commerce:frontendv1.0.4
    container_name: frontend
    expose:
      - "80"
    depends_on:
      - products-service
      - orders-service
      - payments-service
      - users-service
    networks:
      - ecommerce-net
    restart: always

  # === NGINX GATEWAY (Reverse Proxy) ===
  nginx-gateway:
    image: nginx:alpine
    container_name: nginx-gateway
    ports:
      - "8080:80"  # Puerto público principal
    volumes:
      - ./nginx-gateway/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - frontend
      - products-service
      - orders-service
      - payments-service
      - users-service
    networks:
      - ecommerce-net
    restart: always

# === NETWORK ===
networks:
  ecommerce-net:
    driver: bridge



🚀 Cómo Ejecutarlo
Debes descargar el archivo docker-compose.yml que se encuentra en /infra/DockerCompose/docker-compose.yml
Tambien en el lugar donde tengas este archivo debes crear una carpeta llamada /nginx-gateway y dentro de esta debes tener el archivo nginx.conf
archivo nginx.conf
events {}

http {
  sendfile on;
  client_max_body_size 10m;

  server {
    listen 80;
    server_name _;

    # === Servicios API ===
    location /products/ {
      proxy_pass http://products-service:8081/;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
    }

    location /orders/ {
      proxy_pass http://orders-service:8083/;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
    }

    location /payments/ {
      proxy_pass http://payments-service:8082/;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
    }

    location /users/ {
      proxy_pass http://users-service:8084/;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
    }

    # === Frontend ===
    location / {
      proxy_pass http://frontend:80/;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      try_files $uri /index.html;
    }
  }
}
Luego simplemente ejecuta -> docker compose up -d
🧪 Cómo Probar el Flujo Completo

Crear un producto → POST /products

Crear un pedido → POST /orders

El orders-service consulta products-service y luego invoca payments-service

payments-service procesa el pago y envía una notificación

El notifications-service registra el evento en log o lo reenvía al frontend

Puedes usar Postman para probar cada endpoint individualmente.

🛠️ Próximos Pasos

 Desplegar en Kubernetes / Tanzu

 Añadir observabilidad (Prometheus + Grafana)

 Implementar colas de mensajería (RabbitMQ o Kafka)

 Agregar base de datos a cada microservicio (MySQL / PostgreSQL)

 Pipeline CI/CD con GitHub Actions

👨‍💻 Autor

Juan Andrés González
📍 Paraguay

