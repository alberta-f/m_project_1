# hotel/services/booking_service.py
from hotel.models import Booking
from datetime import date

def is_room_available(room, start_date: date, end_date: date) -> bool:
    return not Booking.objects.filter(
        room=room,
        start_date__lt=end_date,
        end_date__gt=start_date
    ).exists()
