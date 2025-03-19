from rest_framework import serializers
from .models import HotelRoom, Booking
from .booking_service import is_room_available

class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True


class HotelRoomSerializer(BaseSerializer):
    class Meta:
        model = HotelRoom
        fields = '__all__'


class BookingSerializer(BaseSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
    
    def validate(self, data):
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError(
                'Дата начала должна быть раньше даты окончания'
            )
        
        if not is_room_available(data['room'], data['start_date'], data['end_date']):
            raise serializers.ValidationError(
                'Номер занят в указанные даты'
            )
        return data
    