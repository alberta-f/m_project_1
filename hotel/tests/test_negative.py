from rest_framework.test import APITestCase
from hotel.models import HotelRoom, Booking


class HotelRoomNegativeAPITest(APITestCase):
    def setUp(self):
        self.room = HotelRoom.objects.create(price_per_night=500,
                                             created_at='2025-01-01')


    def test_get_nonexistent_room(self):
        response = self.client.get('/rooms/999/')

        self.assertEqual(response.status_code, 404)


    def test_update_nonexistent_room(self):
        data = {'price_per_night': 999}

        response = self.client.put('/rooms/999/', 
                                   data, 
                                   format='json')
        self.assertEqual(response.status_code, 404)

    
    def test_delete_nonexistent_room(self):
        response = self.client.delete('/rooms/999/')

        self.assertEqual(response.status_code, 404)


class BookingNegativeAPITest(APITestCase):
    def setUp(self):
        self.room = HotelRoom.objects.create(price_per_night=500, 
                                             created_at='2025-01-01')


    def test_create_booking_invalid_dates(self):
        data = {
            'room': self.room.id,
            'start_date': '2025-01-10',
            'end_date': '2025-01-05'
        }
        response = self.client.post('/bookings/', 
                                    data, 
                                    format='json')
        
        self.assertEqual(response.status_code, 400)
    

    def test_get_nonexistent_booking(self):
        response = self.client.get('/bookings/999/')

        self.assertEqual(response.status_code, 404)
    

    def test_update_nonexistent_booking(self):
        data = {
            'room': self.room.id,
            'start_date': '2025-01-10',
            'end_date': '2025-01-15'
        }

        response = self.client.put('/bookings/999/', 
                                   data, 
                                   format='json')
        
        self.assertEqual(response.status_code, 404)
    

    def test_update_invalid_data(self):
        booking = Booking.objects.create(
            room=self.room,
            start_date='2025-01-10',
            end_date='2025-01-15')
        
        data = {
            'room': self.room.id,
            'start_date': '2024-01-10',
            'end_date': '2025-01-15'
        }

        response = self.client.put(f'/bookings/{booking.id}/', 
                                   data, 
                                   format='json')
        self.assertEqual(response.status_code, 400)

    
    def test_delete_nonexistent_booking(self):
        response = self.client.delete('/bookings/999/')

        self.assertEqual(response.status_code, 404)
