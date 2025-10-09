from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/notifications", tags=["Notifications"])


class NotificationRequest(BaseModel):
    email: EmailStr
    subject: str
    message: str


@router.post("/send")
def send_notification(notification: NotificationRequest):
    # Simulamos envío de correo (en el futuro esto se conectará a Mailtrap o SMTP)
    print(f"📧 Simulated email sent to {notification.email}")
    print(f"Subject: {notification.subject}")
    print(f"Message: {notification.message}")

    return {
        "status": "success",
        "detail": f"Notification sent to {notification.email}"
    }
