from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from django.utils import timezone
from django.conf import settings

#! Time and date functonality dont work

class TodoemEncryption:
    
    _data = None
    _token = None
    _date = None
    
    def __init__(self, data: str = None, token: str = None) -> None:
        self._key = settings.VERIFICATION_KEY.encode()
        self._algo = Fernet(self._key)
        self._token = token
        self._data = data
    
    
    @property
    def key(self) -> str:
        return self._key.decode()
    
    @property
    def data(self) -> str:
        return self._data
    
    @property
    def token(self) -> str:
        return self._token
    
    @property
    def date(self) -> datetime:
        return self._date
    
    
    def encrypt_with_date(self, data: str = None, day: int = 3) -> str:
        if data is None: 
            assert self._data is not None, 'data not provided'
            data = self._data
        self._date = timezone.now() + timedelta(days=day)
        token = self._algo.encrypt(f"{data}|{self._date.strftime('%Y-%m-%d %H:%M:%S')}".encode())
        self._token = token.decode()
        return self._token
    
    
    def decrypt_with_date(self, token: str = None) -> tuple[str, datetime]:
        raw = self.decrypt(token=token)
        sep = raw.split('|') 
        self._data = sep[0]
        self._date = datetime.strptime(sep[1], '%Y-%m-%d %H:%M:%S')
        return (self._data, self._date)
    
    
    def encrypt(self, data: str = None) -> str:
        if data is None: 
            assert self._data is not None, 'data not provided'
            data = self._data
        token = self._algo.encrypt(data.encode())
        self._token = token.decode()
        return self._token
    
    
    def decrypt(self, token: str = None) -> str:
        if token is None: 
            assert self._token is not None, 'token not provided'
            token = self._token
        self._data = self._algo.decrypt(token.encode()).decode()
        return self._data
    
    
    def is_expired(self, date: datetime = None) -> bool:
        if date is None: 
            assert self._date is not None, 'date not provided'
            date = self._date
        return timezone.now() > date