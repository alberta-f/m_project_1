from django.db import models

# Create your models here.
class HotelRoom(models.Model):
    price_per_night = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)


class Booking(models.Model):
    room = models.ForeignKey(HotelRoom, 
                             related_name='bookings', 
                             on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
