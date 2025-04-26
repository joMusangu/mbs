import qrcode
import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=50, blank=True, null=True)  
    last_name = models.CharField(max_length=50, blank=True, null=True)   

    def __str__(self):
        return self.email
    
class Movies(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    genre = models.CharField(max_length=50)
    director = models.CharField(max_length=100)
    poster_url = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
    
class Home_page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # image = models.ImageField(upload_to='home_page_images/')
    
    def __str__(self):
        return self.title
    
class Payment(models.Model):
    PAYMENT_METHODS = [
        ('CARD', 'Card'),
        ('PAYPAL', 'PayPal'),
        ('APPLE_PAY', 'Apple Pay'),
        ('GOOGLE_PAY', 'Google Pay'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('FAILED', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')  
    amount = models.DecimalField(max_digits=10, decimal_places=2)  
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')  
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.CharField(max_length=255)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Order {self.id} - {self.movie}"

class Ticket(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='ticket')
    show_time = models.DateTimeField()
    qr_code_path = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='VALID')

    def __str__(self):
        return f"Ticket for {self.order.user.email} - {self.order.movie} at {self.show_time}"


# Signal to generate ticket and QR code upon payment confirmation
@receiver(post_save, sender=Payment)
def generate_ticket_and_qr_code(sender, instance, **kwargs):
    if instance.status == 'CONFIRMED':
        # Create a ticket for the order
        order = Order.objects.filter(user=instance.user).last()  # Assuming the latest order
        if order:
            ticket = Ticket.objects.create(order=order, show_time=order.purchase_date)

            # Generate QR code
            qr_data = f"Order ID: {order.id}, Movie: {order.movie}, User: {order.user.email}"
            qr_image = qrcode.make(qr_data)

            # Save QR code image
            qr_code_path = f"media/qr_codes/ticket_{ticket.id}.png"
            os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)
            qr_image.save(qr_code_path)

            # Update ticket with QR code path
            ticket.qr_code_path = qr_code_path
            ticket.save()
