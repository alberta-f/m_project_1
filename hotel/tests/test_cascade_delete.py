from rest_framework.test import APITestCase
from hotel.models import HotelRoom, Booking


class HotelRoomCascadeDeleteAPITest(APITestCase):
    def setUp(self):
        self.room = HotelRoom.objects.create(price_per_night=500, 
                                             created_at='2025-01-01')
        
        Booking.objects.create(
            room=self.room,
            start_date='2025-01-10',
            end_date='2025-01-15'
        )

        Booking.objects.create(
            room=self.room,
            start_date='2025-01-20',
            end_date='2025-01-25'
        )


    def test_delete_room_cascades_to_bookings(self):
        self.assertEqual(Booking.objects.count(), 2)

        response = self.client.delete(f'/rooms/{self.room.id}/')
        self.assertEqual(response.status_code, 204)

        self.assertEqual(Booking.objects.count(), 0)
