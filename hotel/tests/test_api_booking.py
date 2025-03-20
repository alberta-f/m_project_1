from rest_framework.test import APITestCase
from hotel.models import HotelRoom, Booking


class BookingAPITest(APITestCase):
    def setUp(self):
        self.room = HotelRoom.objects.create(price_per_night=500,
                                             created_at='2025-03-10')
        
        self.booking = Booking.objects.create(room=self.room,
                                              start_date='2025-05-10',
                                              end_date='2025-05-11')
        
    def test_get_booking_list(self):
        responce = self.client.get('/bookings/')
        
        self.assertEqual(responce.status_code, 200)
        self.assertEqual(len(responce.data), 1)

    def test_get_booking_single(self):
        responce = self.client.get(f'/bookings/{self.booking.id}/')
        
        self.assertEqual(responce.status_code, 200)
        self.assertEqual(responce.data['room'], self.room.id)


    def test_create_booking_success(self):
        data = {
            'room': self.room.id,
            'start_date': '2025-03-15',
            'end_date': '2025-03-20'
        }

        responce = self.client.post('/bookings/', 
                                    data,
                                    format='json')
        
        self.assertEqual(responce.status_code, 201)
        self.assertEqual(Booking.objects.count(), 2)

    
    def test_create_booking_overlap(self):
        Booking.objects.create(
            room=self.room,
            start_date='2025-03-15',
            end_date='2025-03-20'
        )
        
        data = {
            'room': self.room.id,
            'start_date': '2025-03-13',
            'end_date': '2025-03-21'
        }

        responce = self.client.post('/bookings/', 
                                    data,
                                    format='json')
        
        self.assertEqual(responce.status_code, 400)


    def test_create_booking_before_room_creation(self):
        data = {
            'room': self.room.id,
            'start_date': '2025-03-03',
            'end_date': '2025-03-21'
        }

        responce = self.client.post('/bookings/', 
                                    data,
                                    format='json')
        
        self.assertEqual(responce.status_code, 400)

    
    def test_update_booking(self):
        data = {
            'room': self.room.id,
            'start_date': '2025-03-16',
            'end_date': '2025-03-20'
        }
        response = self.client.put(f'/bookings/{self.booking.id}/', 
                                   data, 
                                   format='json')

        self.assertEqual(response.status_code, 200)

        self.booking.refresh_from_db()
        self.assertEqual(str(self.booking.start_date), '2025-03-16')


    def test_delete_booking(self):
        response = self.client.delete(f'/bookings/{self.booking.id}/')

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())
