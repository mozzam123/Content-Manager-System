from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=15)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=6)

    AUTHOR = 'author'
    ADMIN = 'admin'

    # Define a 'role' field to distinguish between 'admin' and 'author'
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (AUTHOR, 'Author'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=AUTHOR)

    class Meta: 
        managed = True

    def save(self, *args, **kwargs): 
        self.username = self.email
        return super().save(*args, **kwargs)
    


class ContentItem(models.Model):
    content_id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    title = models.CharField(max_length=30)
    body = models.CharField(max_length=300)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contentItem')
    summary = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20, blank=True)


    def __str__(self):
        return self.author.email
    


    