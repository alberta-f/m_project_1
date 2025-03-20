from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import HotelRoom, Booking
from .serializers import HotelRoomSerializer, BookingSerializer
from .services.room_service import sort_rooms, filter_rooms


# Create your views here.
class BaseCRUDView(APIView):
    model = None
    serializer_class = None

    
    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)

        except self.model.DoesNotExist:
            return None
        

    def get_one(self, request, pk):
        instance = self.get_object(pk)

        if instance:
            serializer = self.serializer_class(instance)

            return Response(serializer.data, 
                        status=status.HTTP_200_OK)

        return Response({'error': 'Not found'}, 
                        status=status.HTTP_404_NOT_FOUND)
    

    def get(self, request, pk=None):
        if pk:
            return self.get_one(request, pk)
        
        queryset = self.model.objects.all()

        serializer = self.serializer_class(queryset, many=True)
        
        return Response(serializer.data, 
                        status=status.HTTP_200_OK)
    

    def put(self, request, pk):
        instance = self.get_object(pk)

        if instance:
            serializer = self.serializer_class(instance, data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)
        
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, 
                            status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        instance = self.get_object(pk)

        if instance:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'error': 'Not found'}, 
                        status=status.HTTP_404_NOT_FOUND)


class HotelRoomCRUDView(BaseCRUDView):
    model = HotelRoom
    serializer_class = HotelRoomSerializer


    def get(self, request, pk=None):
        if pk:
            return self.get_one(request, pk)
        
        sort_by = request.query_params.get('sort_by')
        order = request.query_params.get('order', 'asc')

        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')

        queryset = self.model.objects.all()
        
        queryset = filter_rooms(queryset, 
                                min_price=min_price, 
                                max_price=max_price)
        queryset = sort_rooms(queryset, sort_by, order)

        serializer = self.serializer_class(queryset, many=True)
        
        return Response(serializer.data, 
                        status=status.HTTP_200_OK)


class BookingCRUDView(BaseCRUDView):
    model = Booking
    serializer_class = BookingSerializer
