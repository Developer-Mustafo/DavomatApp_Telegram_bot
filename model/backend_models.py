from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, ConfigDict
from datetime import date

T = TypeVar('T')


# Model for the nested 'data' object
class User(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: str
    password: str
    phoneNumber: str
    role: str
    payedDate: Optional[date] = None  # Can be None


# Model for the entire response
class ApiResponse(BaseModel, Generic[T]):
    code: int
    data: Optional[T] = None
    message: Optional[str] = None

    # Pydantic v2 uchun to'g'ri konfiguratsiya
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Balance(BaseModel):
    limit: Optional[date] = None  # Agar limit sanani ifodalasa
    # yoki agar bu miqdorni ifodalasa:
    # limit: Optional[float] = None
    telegramUserId: Optional[int] = None


class BalanceResponse(BaseModel):
    limit: Optional[date] = None
    telegramUserId: Optional[int] = None


class TelegramUser(BaseModel):
    telegramUserId: int
    firstName: str
    lastName: str
    phoneNumber: str


class TelegramUserResponse(BaseModel):
    id: Optional[int] = None
    userId: Optional[int] = None
    telegramUserId: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phoneNumber: Optional[str] = None