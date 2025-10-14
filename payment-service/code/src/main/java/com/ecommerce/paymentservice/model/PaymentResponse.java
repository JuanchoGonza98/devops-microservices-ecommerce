package com.ecommerce.paymentservice.model;

public class PaymentResponse {

    private int orderId;
    private String status;
    private String message;

    public PaymentResponse(int orderId, String status, String message) {
        this.orderId = orderId;
        this.status = status;
        this.message = message;
    }

    public int getOrderId() {
        return orderId;
    }

    public String getStatus() {
        return status;
    }

    public String getMessage() {
        return message;
    }
}
