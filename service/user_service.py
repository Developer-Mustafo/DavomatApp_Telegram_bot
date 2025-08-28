from model import User
import requests
from config import BASE_URL

def pay_to_user(user_id:int, amount:int):

    pass

def register_to_telegram(user:User):

    pass

def get_by_phone_number(phone_number:str):
    """

    :param phone_number:
    :return:password through backend
    """
    return '1234567'

def get_user(user_id:int):
    return [User(user_id, first_name='', last_name='', phone_number='dsda')]
