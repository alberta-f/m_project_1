from django.test import TestCase

from hotel.models import HotelRoom, Booking
from hotel.services.booking_service import is_room_available, is_room_exists

from datetime import date


class BookingServiceTest(TestCase):
    def setUp(self):
        self.room_1 = HotelRoom.objects.create(price_per_night=340, 
                                               created_at='2025-01-02')
        self.room_2 = HotelRoom.objects.create(price_per_night=500)


    def test_room_1_exists(self):
        exist = is_room_exists(self.room_1, date(2025, 1, 3))
        self.assertTrue(exist)

    def test_room_2_exists(self):
        exist = is_room_exists(self.room_2, date(2025, 5, 25))
        self.assertTrue(exist)

    
    def test_room_1_not_exists(self):
        exist = is_room_exists(self.room_1, date(2025, 1, 1))
        self.assertFalse(exist)

    def test_room_2_not_exists(self):
        exist = is_room_exists(self.room_2, date(2025, 1, 1))
        self.assertFalse(exist)


    def test_room_1_available(self):
        available = is_room_available(self.room_1, date(2025, 1, 2), date(2025, 1, 10))
        self.assertTrue(available)
    
    def test_room_2_available(self):
        available = is_room_available(self.room_2, date(2025, 5, 25), date(2025, 5, 26))
        self.assertTrue(available)
    

    def test_room_1_is_not_available(self):
        Booking.objects.create(
            room=self.room_1,
            start_date='2025-01-08',
            end_date='2025-01-12'
        )

        available = is_room_available(self.room_1, date(2025, 1, 2), date(2025, 1, 10))
        self.assertFalse(available)

    def test_room_2_is_not_available(self):
        Booking.objects.create(
            room=self.room_2,
            start_date='2025-05-26',
            end_date='2025-05-29'
        )

        available = is_room_available(self.room_2, date(2025, 5, 24), date(2025, 5, 27))
        self.assertFalse(available)
