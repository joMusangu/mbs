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
    

