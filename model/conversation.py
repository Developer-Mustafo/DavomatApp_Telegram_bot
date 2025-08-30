from dataclasses import dataclass

@dataclass
class Conversation:
    user_id:int
    message:str
    def __init__(self, user_id:int, message:str):
        self.user_id=user_id
        self.message=message
    def __str__(self):
        return f'id={self.user_id}, message={self.message}'