from datetime import date


def to_date(date_):
    if isinstance(date_, str):
        return date.fromisoformat(date_) 
    
    return date_
