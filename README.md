# Hotel Booking API

## 🚀 Быстрый старт проекта

Клонировать проект:
   ```bash
   git clone https://github.com/yourname/hotel_booking.git
   cd hotel_booking
   ```

### Создайте .env:

```bash
POSTGRES_DB=hotel_dbPOSTGRES_USER=hotel_user
POSTGRES_PASSWORD=hotel_pass
DATABASE_URL=postgres://hotel_user:hotel_pass@db:5432/hotel_db
DEBUG=True
```
### Запустите проект:

```bash
docker-compose --env-file .env up --build
```

### 📬 API эндпоинты
## /rooms/
- GET /rooms/ — список номеров
- POST /rooms/ — создать номер
- GET /rooms/{id}/ — получить номер по id
- PUT /rooms/{id}/ — обновить номер
- DELETE /rooms/{id}/ — удалить номер

## /bookings/
- GET /bookings/ — список бронирований
- POST /bookings/ — создать бронь
- GET /bookings/{id}/ — получить бронь
- PUT /bookings/{id}/ — обновить бронь
- DELETE /bookings/{id}/ — удалить бронь
