from django.core.mail import send_mail

def send_invoice_email(order):
    send_mail(
        subject=f"Invoice #{order.id}",
        message=f"Your invoice total is {order.total}",
        from_email="aun85423@gmail.com",
        recipient_list=[order.client.email],
        fail_silently=False,
    )