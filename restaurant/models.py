from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    is_gourmet = models.BooleanField(default=False)
    is_cook = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

class TimeSlot(models.Model):
    date=models.DateField(default=None)
    time=models.TimeField(default=None)
    available=models.BooleanField(default=True)

    def __str__(self):
        return str(self.date) + " " + str(self.time)
    
class Reservation(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    time_slot=models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    number_of_people=models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " - " + str(self.time_slot) + " for " + str(self.number_of_people) + " people"

class Cuisine(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    image = models.ImageField(upload_to='cuisines/')

    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.cuisine.name}"