from django.db import models

# Create your models here.
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

    def __str__(self):
        return self.title
    
class Home_page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='home_page_images/')
    
    def __str__(self):
        return self.title
    
class feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.email} on {self.created_at}"
    

