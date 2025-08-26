class User:
    def __init__(self, user_id:int, first_name:str, last_name:str, phone_number:str):
        self.user_id=user_id
        self.first_name=first_name
        self.last_name=last_name
        self.phone_number=phone_number
    def __str__(self):
        return f'User(id={self.user_id}, first_name={self.first_name}, last_name={self.last_name}, phone_number={self.phone_number})'