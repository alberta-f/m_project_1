from datetime import date


def to_date(date_):
    """
    Получает дату в str или date
    -> в date формате
    """
    
    if isinstance(date_, str):
        return date.fromisoformat(date_) 
    
    return date_

