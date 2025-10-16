package com.ecommerce.paymentservice.service;

import com.ecommerce.paymentservice.model.PaymentRequest;
import com.ecommerce.paymentservice.model.PaymentResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;

@Service
public class PaymentService {

    private final RestTemplate restTemplate = new RestTemplate();
    private static final String ORDERS_API_URL = "http://orders-service:8083/orders";

    public PaymentResponse processPayment(PaymentRequest request) {
        // 1️⃣ Validar la existencia de la orden
        String orderUrl = ORDERS_API_URL + "/" + request.getOrder_id();
        ResponseEntity<Object> orderResponse = restTemplate.getForEntity(orderUrl, Object.class);

        if (orderResponse.getStatusCode() != HttpStatus.OK) {
            return new PaymentResponse(
                    request.getOrder_id(),
                    "FAILED",
                    "Order not found"
            );
        }

        // 2️⃣ Simular procesamiento del pago
        try {
            Thread.sleep(1000); // simula tiempo de procesamiento
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        // 3️⃣ Enviar notificación simple (simulada)
        String notification = String.format(
                "✅ Payment completed for order #%d, amount: %.2f",
                request.getOrder_id(),
                request.getAmount()
        );

        System.out.println(notification);

        // 4️⃣ Devolver respuesta
        return new PaymentResponse(
                request.getOrder_id(),
                "Payment successful",
                notification
        );
    }
}
