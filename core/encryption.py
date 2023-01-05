from cryptography.fernet import Fernet
from datetime import timedelta
from django.conf import settings

from .dt import TodoemDT

KEY = settings.VERIFICATION_KEY.encode()
ALGO = Fernet(KEY)
class TodoemEncryption:
    """
    A class for encrypting and decrypting data using the "ALGO" algorithm.
    """
    EXPIRED_PERIOD = timedelta(days=3)
    
    @staticmethod
    def encrypt(data: str) -> str:
        """
        Encrypts a string using the "ALGO" algorithm.
        
        Args:
            data: The string to encrypt.
            
        Returns:
            The encrypted string.
        """
        return ALGO.encrypt(data.encode()).decode()
    
    @staticmethod
    def decrypt(token: str) -> str:
        """
        Decrypts a string using the "ALGO" algorithm.
        
        Args:
            token: The encrypted string to decrypt.
            
        Returns:
            The decrypted string.
        """
        return ALGO.decrypt(token.encode()).decode()
    
    @staticmethod
    def format_dict(data: dict[str,str]):
        '''
        Format dict -> str to encrypt 
        
        format 'key1:|:value1;;key2:|:value2;;...;;keyn:|:valuen'
        
        avoid using special charecters: ':|:' and ';;' in data
        
        Args:
            data: The dictionary to format.
            
        Returns:
            The formatted string.
        
        Raises:
            Exception: If the dictionary is empty.
        '''
        if not data:
            raise Exception('data is empty')
        
        raw_list = []
        for key, value in data.items():
            raw_list.append(f'{key}:|:{value}')
        
        return ";;".join(raw_list)
    
    @staticmethod 
    def deformat_dict(data: str) -> dict:
        """
        Deformats a formatted string as a dictionary.
        
        Args:
            data: The formatted string to deformat.
            
        Returns:
            The deformatted dictionary.
        """
        result = {}
        statements = data.split(';;')
        for statement in statements:
            temp = statement.split(':|:')
            result[temp[0]] = temp[1]
        return result
    
    
    @classmethod
    def encrypt_dict(cls, data: dict[str, str], expire: bool=False, delta: timedelta|None=None):
        """
        Encrypts a dictionary using the "ALGO" algorithm.
        
        Args:
            data: The dictionary to encrypt.
            expire (optional): A flag indicating whether the encrypted data should include an expiration date. Default is False.
            delta (optional): The expiration period for the encrypted data, in the form of a timedelta. If not provided, the default expiration period will be used "EXPIRED_PERIOD".
        
        Returns:
            The encrypted string.
        """
        if expire:
            data['expire'] = TodoemDT.now_delta(delta=cls.EXPIRED_PERIOD if delta is None else delta, string=True)

        str_data = cls.format_dict(data)
        return cls.encrypt(str_data)
    
    @classmethod
    def decrypt_dict(cls, token: str) -> tuple[dict, bool]:
        """
        Decrypts a string using the "ALGO" algorithm and returns the corresponding dictionary.
        
        Args:
            token: The encrypted string to decrypt.
            
        Returns:
            A tuple containing the decrypted dictionary and a boolean indicating whether the data is still valid (i.e. has not expired).
        """
        raw_data = cls.decrypt(token)
        data = cls.deformat_dict(raw_data)
        expire = data.get('expire', None)
        if expire is not None:
            return data, TodoemDT.compare(expire, '>')
        return data, True



class TodoemTokenError(Exception):
    pass