from django.db import models
from datetime import date

# Create your models here.
class HotelRoom(models.Model):
    price_per_night = models.IntegerField()
    created_at = models.DateField(default=date.today)


class Booking(models.Model):
    room = models.ForeignKey(HotelRoom, 
                             related_name='bookings', 
                             on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
