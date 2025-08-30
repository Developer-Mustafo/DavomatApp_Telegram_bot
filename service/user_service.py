from datetime import date
from typing import List
import requests
from dateutil.relativedelta import relativedelta
from config import BASE_URL
from model import (User, ApiResponse, Person, Balance, TelegramUser, TelegramUserResponse)

monthly_payment = 20_000


def pay_to_user(user_id: int, amount: int):
    # Avval balans ma'lumotlarini olish
    url_balance = f'{BASE_URL}/api/student/balance?telegramUserId={user_id}'
    response = requests.get(url_balance)
    response_json = response.json()

    # ApiResponse ni pars qilish
    api_response = ApiResponse[Balance](**response_json)

    if api_response.data is None:
        # Agar balans mavjud bo'lmasa, yangi limitni hisoblash
        total_months = amount / monthly_payment
        # Hozirgi sanadan boshlab
        current_date = date.today()
        years = int(total_months // 12)
        remaining_months = total_months % 12
        months = int(remaining_months)
        days = int((remaining_months - months) * 30)

        # Yangi limitni hisoblash
        new_limit = current_date + relativedelta(years=years, months=months, days=days)
    else:
        # Mavjud limitdan davom etish
        old_limit = api_response.data.limit
        if old_limit is None or old_limit<date.today():
            old_limit = date.today()
        total_months = amount / monthly_payment
        years = int(total_months // 12)
        remaining_months = total_months % 12
        months = int(remaining_months)
        days = int((remaining_months - months) * 30)

        new_limit = old_limit + relativedelta(years=years, months=months, days=days)

    # Balance obyektini yaratish
    balance = Balance(limit=new_limit, telegramUserId=user_id)

    # JSON ga aylantirish
    body_json = balance.model_dump_json()  # Pydantic v2 uchun

    url = f'{BASE_URL}/api/user/pay'
    response = requests.put(url, data=body_json, headers={'Content-Type': 'application/json'})

    print('------------------------------')
    return response


def register_to_telegram(user: User):
    telegram_user = TelegramUser(
        telegramUserId=user.user_id,  # user.user_id emas, user.id bo'lishi kerak
        firstName=user.first_name,
        lastName=user.last_name,
        phoneNumber=user.phone_number
    )

    body_json = telegram_user.model_dump_json()  # Pydantic v2 uchun

    url = f'{BASE_URL}/api/telegram/register'
    response = requests.post(url, data=body_json, headers={'Content-Type': 'application/json'})
    response_json = response.json()

    api_response = ApiResponse[TelegramUser](**response_json)
    print(api_response)
    return api_response


def get_by_phone_number(phone_number: str):
    """
    :param phone_number:
    :return: password through backend
    """
    url = f'{BASE_URL}/api/user/phone/{phone_number}'
    response = requests.get(url)

    if response.status_code != 200:
        return None

    response_json = response.json()
    api_response = ApiResponse[Person](**response_json)
    print(api_response)

    person: Person = None
    if api_response.code == 200:
        person = api_response.data
    return person


def get_user_list():
    url = f'{BASE_URL}/api/telegram/get_all_users'
    response = requests.get(url)

    if response.status_code != 200:
        return []

    response_json = response.json()
    api_response = ApiResponse[List[TelegramUserResponse]](**response_json)

    if api_response.code == 200 and api_response.data:
        return api_response.data
    return []