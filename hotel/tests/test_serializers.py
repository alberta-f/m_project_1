from django.test import TestCase

from hotel.models import HotelRoom
from hotel.serializers import BookingSerializer


class BookingSerializerTest(TestCase):
    def setUp(self):
        self.room = HotelRoom.objects.create(price_per_night=340, 
                                             created_at='2025-01-02')

    def test_valid_serializer(self):
        data = {
            'room': self.room.id,
            'start_date': '2025-01-05',
            'end_date': '2025-01-10'
        }
        serializer = BookingSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_if_end_before_start(self):
        data = {
            'room': self.room.id,
            'start_date': '2025-01-10',
            'end_date': '2025-01-05'
        }
        serializer = BookingSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Дата начала должна быть раньше даты окончания', 
                      str(serializer.errors))

    def test_invalid_if_room_not_exist(self):
        data = {
            'room': self.room.id,
            'start_date': '2024-12-30',
            'end_date': '2025-01-05'
        }
        serializer = BookingSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Нельзя бронировать комнату до ее создания', 
                      str(serializer.errors['non_field_errors'][0]))

