package com.ecommerce.paymentservice.model;

public class PaymentResponse {
    private int order_id;
    private String status;
    private String message;

    public PaymentResponse(int order_id, String status, String message) {
        this.order_id = order_id;
        this.status = status;
        this.message = message;
    }

    public int getOrder_id() {
        return order_id;
    }

    public String getStatus() {
        return status;
    }

    public String getMessage() {
        return message;
    }
}
