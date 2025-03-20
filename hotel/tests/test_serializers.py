from django.test import TestCase

from hotel.models import HotelRoom
from hotel.serializers import BookingSerializer, HotelRoomSerializer

from datetime import date


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


class HotelRoomSerializerTest(TestCase):
    def test_create_room_with_default_created_at(self):
        data = {
            'price_per_night': 500
        }
        serializer = HotelRoomSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        room = serializer.save()

        self.assertEqual(room.price_per_night, 500)
        self.assertEqual(room.created_at, date.today())
    

    def test_created_at_cannot_be_in_future(self):
        future_date = (date.today().replace(year=date.today().year + 1)).isoformat()

        data = {
            'price_per_night': 500,
            'created_at': future_date
        }

        serializer = HotelRoomSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('Дата создания не может быть в будущем', str(serializer.errors))


    def test_create_room_with_custom_created_at(self):
        data = {
            'price_per_night': 500,
            'created_at': '2025-01-01'
        }
        serializer = HotelRoomSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        room = serializer.save()

        self.assertEqual(room.created_at, date(2025, 1, 1))
