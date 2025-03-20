from rest_framework import serializers

from .models import HotelRoom, Booking
from .services.booking_service import is_room_available, is_room_exists
from .utils import to_date

from datetime import date


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True


class HotelRoomSerializer(BaseSerializer):
    """
    Сериализует для модели HotelRoom
    
    Валидирует:
        -created_at не находится в будущем
    """

    class Meta:
        model = HotelRoom
        fields = '__all__'

    def validate_created_at(self, value):
        """
        Проверяет, что created_at не находится в будущем
        """

        if date.today() < value:
            raise serializers.ValidationError(
                'Дата создания не может быть в будущем'
            )
        
        return value


class BookingSerializer(BaseSerializer): 
    """
    Сериализатор для модели Booking
    
    Валидирует:
        - даты бронирования (start_date < end_date)
        - наличие комнаты к моменту бронирования
        - отсутствие пересечений даты
    """
    
    class Meta:
        model = Booking
        fields = '__all__'
    
    def validate(self, data):
        start_date = to_date(data['start_date'])
        end_date = to_date(data['end_date'])

        if end_date <= start_date:
            raise serializers.ValidationError(
                'Дата начала должна быть раньше даты окончания'
            )
        
        if not is_room_exists(data['room'],
                              start_date):
            raise serializers.ValidationError(
                'Нельзя бронировать комнату до ее создания'
            )
        
        if not is_room_available(data['room'], 
                                 start_date, 
                                 end_date):
            
            raise serializers.ValidationError(
                'Номер занят в указанные даты'
            )
        
        return data
    