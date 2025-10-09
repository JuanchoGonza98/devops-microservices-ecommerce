package com.ecommerce.paymentservice.service;

import com.ecommerce.paymentservice.model.Order;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class PaymentService {

    private static final String ORDERS_SERVICE_URL = "http://orders-service:8083/orders/";

    @Autowired
    private RestTemplate restTemplate;

    public String processPayment(int orderId) {
        // Llamar al orders-service
        Order order = restTemplate.getForObject(ORDERS_SERVICE_URL + orderId, Order.class);

        if (order == null) {
            return " Order not found!";
        }

        // Simulamos validación y procesamiento del pago
        if (order.getTotal() <= 0) {
            return " Invalid order amount!";
        }

        return " Payment processed for order ID " + order.getId() + " (total: $" + order.getTotal() + ")";
    }
}
