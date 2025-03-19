from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import HotelRoom, Booking
from .serializers import HotelRoomSerializer, BookingSerializer


# Create your views here.
class BaseCRUDView(APIView):
    model = None
    serializer_class = None

    
    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)

        except self.model.DoesNotExist:
            return None
        

    def get(self, request, pk=None):
        if pk is not None:
            instance = self.get_object(pk)

            if instance is None:
                return Response({'error': 'Not found'}, 
                                status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.serializer_class(instance)
        
        else:
            queryset = self.model.objects.all()
            serializer = self.serializer_class(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def put(self, request, pk):
        instance = self.get_object(pk)

        if instance:
            serializer = self.serializer_class(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        instance = self.get_object(pk)

        if instance:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class HotelRoomCRUDView(BaseCRUDView):
    model = HotelRoom
    serializer_class = HotelRoomSerializer


class BookingCRUDView(BaseCRUDView):
    model = Booking
    serializer_class = BookingSerializer
