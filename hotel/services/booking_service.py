from hotel.models import Booking
from hotel.utils import to_date
from datetime import date

def is_room_available(room, start_date: date, end_date: date) -> bool:
    return not Booking.objects.filter(
        room=room,
        start_date__lt=end_date,
        end_date__gt=start_date
    ).exists()


def is_room_exists(room, start_date):
    created_at = to_date(room.created_at)

    return created_at <= start_date
