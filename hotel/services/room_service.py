def sort_rooms(queryset, sort_by, order):
    """
    Сортировка списка номер по полю и порядку
    
    Args:
        queryset: список номеров

        sort_by: поле для сортировки
        ('price_per_night', 'created_at')

        order: направление сортировки
        ('asc', 'desc')
    """

    if sort_by in ('price_per_night', 'created_at'):

        if order == 'desc':
            sort_by = f'-{sort_by}'
        
        return queryset.order_by(sort_by)
    return queryset


def filter_rooms(queryset, min_price=None, max_price=None):
    """
    Фильтрация списка комнат по диапозону цен
    """
    
    if min_price is not None:
        queryset = queryset.filter(price_per_night__gte=min_price)

    if max_price is not None:
        queryset = queryset.filter(price_per_night__lte=max_price)
    
    return queryset
