from django.db import models
from datetime import date


class HotelRoom(models.Model):
    """    
    Модель комнаты отеля.
    Поля:
        price_per_night (int): Цена за одну ночь проживания.        
        created_at (date): Дата создания комнаты. По умолчанию — сегодняшняя дата.
    """

    price_per_night = models.IntegerField()
    created_at = models.DateField(default=date.today)


class Booking(models.Model):
    """
    Модель бронирования номера.

    Поля:
        room (ForeignKey): Ссылка на HotelRoom. При удалении комнаты — каскадное удаление броней.
        start_date (date): Дата начала бронирования.
        end_date (date): Дата окончания бронирования.
    """
    
    room = models.ForeignKey(HotelRoom, 
                             related_name='bookings', 
                             on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

