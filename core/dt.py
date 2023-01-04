from datetime import datetime
from django.utils import timezone

class TodoemDT:
    @staticmethod
    def datetime_to_str(dt: datetime) -> str:
        return dt.isoformat()

    @staticmethod
    def str_to_datetime(dt: str) -> datetime:
        return datetime.fromisoformat(dt)

    @staticmethod
    def now(string: bool=False):
        if string:
            return timezone.now().isoformat()
        
        return timezone.now()
    
    @staticmethod
    def now_delta(delta, string: bool=False):
        if string:
            return (timezone.now()+delta).isoformat()
        
        return timezone.now() + delta
    

    @classmethod
    def compare(cls, dt: str|datetime, comp: str, dt2: str|datetime=None) -> bool:
        if dt2 is None:
            dt2 = timezone.now()
        else:
            dt2 = dt2 if not isinstance(dt2, str) else cls.str_to_datetime(dt2)
        
        dt = dt if not isinstance(dt, str) else cls.str_to_datetime(dt)
        
        match comp:
            case '>':
                return dt >= dt2 
            case '<':
                return dt <= dt2 
            case '=':
                return dt == dt2
            case _:
                raise Exception('invalid comp')       

