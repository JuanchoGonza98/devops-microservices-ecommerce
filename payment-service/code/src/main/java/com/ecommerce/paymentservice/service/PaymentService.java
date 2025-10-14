package com.ecommerce.paymentservice.service;

import com.ecommerce.paymentservice.model.PaymentResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;

import java.util.HashMap;
import java.util.Map;

@Service
public class PaymentService {

    private final RestTemplate restTemplate = new RestTemplate();
    private static final String ORDERS_API_URL = "http://orders-service:8083";
    private static final String NOTIFICATIONS_API_URL = "http://notifications-service:8000";

    public PaymentResponse processPayment(int orderId) {
        try {
            // ✅ 1. Verificar si la orden existe
            ResponseEntity<String> orderResponse =
                    restTemplate.getForEntity(ORDERS_API_URL + "/orders/" + orderId, String.class);

            if (orderResponse.getStatusCode() != HttpStatus.OK) {
                return new PaymentResponse(orderId, "FAILED", "Order not found.");
            }

            // ✅ 2. Simular procesamiento del pago
            Thread.sleep(1000); // Simula una transacción bancaria
            System.out.println("💳 Payment processed for order " + orderId);

            // ✅ 3. Actualizar estado de la orden a PAID
            String updateUrl = ORDERS_API_URL + "/orders/" + orderId + "/status?status=PAID";
            restTemplate.put(updateUrl, null);
            System.out.println("✅ Order " + orderId + " updated to PAID.");

            // ✅ 4. Notificar al notifications-service
            try {
                Map<String, Object> notification = new HashMap<>();
                notification.put("order_id", orderId);
                notification.put("status", "PAID");
                notification.put("message", "Order #" + orderId + " has been paid successfully.");

                restTemplate.postForEntity(
                        NOTIFICATIONS_API_URL + "/notifications/send",
                        notification,
                        String.class
                );
                System.out.println("📨 Notification sent to notifications-service for order " + orderId);

            } catch (Exception notifyEx) {
                System.err.println("⚠️ Could not notify notifications-service: " + notifyEx.getMessage());
            }

            // ✅ 5. Devolver respuesta al cliente
            return new PaymentResponse(orderId, "PAID", "Payment processed successfully for order " + orderId);

        } catch (Exception e) {
            e.printStackTrace();
            return new PaymentResponse(orderId, "FAILED", "Error processing payment: " + e.getMessage());
        }
    }
}
