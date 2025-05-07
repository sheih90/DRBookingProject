from pydantic import BaseModel
from typing import Optional
from datetime import date


class BookingDates (BaseModel):
    checkin: date
    checkout: date

class Booking(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None

class BookingResponse(BaseModel):
    bookingid: int
    booking: Booking

# в данном случае класс BookingResponse отвечает за верхнеуровневые параметры,
# но в нем есть параметры с вложенностью других параметров: в данном случае параметр booking, в котором также есть
# вложенный bookingdates
# таким образом, на каждую вложенность параметров создаем свой класс
# важно писать код как бы "снизу вверх", чтобы pycharm видел вложенные параметры для валидации данных