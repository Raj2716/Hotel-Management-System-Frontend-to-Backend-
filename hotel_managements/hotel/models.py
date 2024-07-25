from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    name=models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    gmail_id = models.EmailField(max_length=254)
   

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    ratings = models.FloatField()
    available_rooms = models.IntegerField()
    price = models.FloatField()
    amenities = models.TextField()
    bed_type = models.CharField(max_length=50)
    hotelier = models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=1)
    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.location = self.location.upper()
        self.amenities = self.amenities.upper()
        self.bed_type = self.bed_type.upper()
        super().save(*args, **kwargs)

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    num_members = models.IntegerField()
    total_price = models.FloatField()

    