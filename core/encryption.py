from cryptography.fernet import Fernet
from datetime import timedelta
from django.conf import settings

from .dt import TodoemDT

KEY = settings.VERIFICATION_KEY.encode()
ALGO = Fernet(KEY)

class TodoemEncryption:
    EXPIRED_PERIOD = timedelta(days=3)
    
    @staticmethod
    def encrypt(data: str) -> str:
        # only for strings
        return ALGO.encrypt(data.encode()).decode()
    
    @staticmethod
    def decrypt(token: str) -> str:
        # only for strings
        return ALGO.decrypt(token.encode()).decode()
    
    @staticmethod
    def format_dict(data: dict[str,str]):
        '''
        Format dict -> str to encrypt 
        
        format 'key1:|:value1;;key2:|:value2;;...;;keyn:|:valuen'
        
        avoid using special charecters: ':|:' and ';;' in data
        '''
        if not data:
            raise Exception('data is empty')
        
        raw_list = []
        for key, value in data.items():
            raw_list.append(f'{key}:|:{value}')
        
        return ";;".join(raw_list)
    
    @staticmethod 
    def deformat_dict(data: str) -> dict:
        # deformatting 
        result = {}
        statements = data.split(';;')
        for statement in statements:
            temp = statement.split(':|:')
            result[temp[0]] = temp[1]
        return result
    
    
    @classmethod
    def encrypt_dict(cls, data: dict[str, str], expire: bool=False, delta: timedelta|None=None):
        if expire:
            data['expire'] = TodoemDT.now_delta(delta=cls.EXPIRED_PERIOD if delta is None else delta, string=True)

        str_data = cls.format_dict(data)
        return cls.encrypt(str_data)
    
    @classmethod
    def decrypt_dict(cls, token: str) -> tuple[dict, bool]:
        raw_data = cls.decrypt(token)
        data = cls.deformat_dict(raw_data)
        expire = data.get('expire', None)
        if expire is not None:
            return data, TodoemDT.compare(expire, '>')
        return data, True



class TodoemTokenError(Exception):
    pass