from rest_framework.test import APITestCase
from hotel.models import HotelRoom


class HotelRoomAPITest(APITestCase):
    def setUp(self):
        self.room1 = HotelRoom.objects.create(price_per_night=300, 
                                              created_at='2025-01-01')
        self.room2 = HotelRoom.objects.create(price_per_night=600)


    def test_create_room(self):
        data = {'price_per_night': 400}

        response = self.client.post('/rooms/', 
                                    data, 
                                    format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(HotelRoom.objects.count(), 3)

    def test_get_room_list(self):
        response = self.client.get('/rooms/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


    def test_get_single_room(self):
        response = self.client.get(f'/rooms/{self.room1.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['price_per_night'], 300)


    def test_update_room(self):
        data = {'price_per_night': 700}

        response = self.client.put(f'/rooms/{self.room1.id}/', 
                                   data, 
                                   format='json')
        
        self.assertEqual(response.status_code, 200)

        self.room1.refresh_from_db()
        self.assertEqual(self.room1.price_per_night, 700)


    def test_delete_room(self):
        response = self.client.delete(f'/rooms/{self.room1.id}/')
        
        self.assertEqual(response.status_code, 204)
        self.assertFalse(HotelRoom.objects.filter(id=self.room1.id).exists())
