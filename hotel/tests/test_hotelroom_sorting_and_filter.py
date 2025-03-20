from rest_framework.test import APITestCase
from hotel.models import HotelRoom


class HotelRoomSortingAPITest(APITestCase):
    def setUp(self):
        self.room1 = HotelRoom.objects.create(price_per_night=300, 
                                              created_at='2025-01-01')
        self.room2 = HotelRoom.objects.create(price_per_night=600, 
                                              created_at='2025-01-03')
        self.room3 = HotelRoom.objects.create(price_per_night=400, 
                                              created_at='2025-01-02')


    def test_sort_by_price_asc(self):
        response = self.client.get('/rooms/?sort_by=price_per_night&order=asc')

        prices = [room['price_per_night'] for room in response.data]
        self.assertEqual(prices, [300, 400, 600])


    def test_sort_by_price_desc(self):
        response = self.client.get('/rooms/?sort_by=price_per_night&order=desc')

        prices = [room['price_per_night'] for room in response.data]
        self.assertEqual(prices, [600, 400, 300])


    def test_sort_by_created_at_asc(self):
        response = self.client.get('/rooms/?sort_by=created_at&order=asc')

        ids = [room['id'] for room in response.data]
        self.assertEqual(ids, [self.room1.id, self.room3.id, self.room2.id])


    def test_sort_by_created_at_desc(self):
        response = self.client.get('/rooms/?sort_by=created_at&order=desc')

        ids = [room['id'] for room in response.data]
        self.assertEqual(ids, [self.room2.id, self.room3.id, self.room1.id])


class HotelRoomFilteringAPITest(APITestCase):
    def setUp(self):
        self.room1 = HotelRoom.objects.create(price_per_night=300, 
                                              created_at='2025-01-01')
        self.room2 = HotelRoom.objects.create(price_per_night=500, 
                                              created_at='2025-01-02')
        self.room3 = HotelRoom.objects.create(price_per_night=700, 
                                              created_at='2025-01-03')


    def test_min_price_filter(self):
        response = self.client.get('/rooms/?min_price=400')

        ids = [room['id'] for room in response.data]
        self.assertEqual(ids, [self.room2.id, self.room3.id])


    def test_max_price_filter(self):
        response = self.client.get('/rooms/?max_price=500')

        ids = [room['id'] for room in response.data]
        self.assertEqual(ids, [self.room1.id, self.room2.id])


    def test_min_and_max_price_filter(self):
        response = self.client.get('/rooms/?min_price=400&max_price=600')
        ids = [room['id'] for room in response.data]
        self.assertEqual(ids, [self.room2.id])
