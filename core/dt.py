from datetime import datetime
from django.utils import timezone

class TodoemDT:
    """
    A class for handling date and time conversions and comparisons.
    """
    @staticmethod
    def datetime_to_str(dt: datetime) -> str:
        """
        Converts a datetime object to a string in ISO format.
        
        Args:
            dt: The datetime object to convert.
            
        Returns:
            The ISO formatted string.
        """
        return dt.isoformat()

    @staticmethod
    def str_to_datetime(dt: str) -> datetime:
        """
        Converts an ISO formatted string to a datetime object.
        
        Args:
            dt: The ISO formatted string to convert.
            
        Returns:
            The corresponding datetime object.
        """
        return datetime.fromisoformat(dt)

    @staticmethod
    def now(string: bool=False):
        """
        Returns the current time in either ISO format (if string is True) or as a datetime object (if string is False).
        
        Args:
            string (optional): A flag indicating whether the current time should be returned as an ISO formatted string or as a datetime object. Default is False.
        
        Returns:
            The current time as either an ISO formatted string or a datetime object.
        """
        if string:
            return timezone.now().isoformat()
        
        return timezone.now()
    
    @staticmethod
    def now_delta(delta, string: bool=False):
        """
        Returns the current time plus a specified time delta in either ISO format (if string is True) or as a datetime object (if string is False).
        
        Args:
            delta: The time delta to add to the current time. This should be a timedelta object.
            string (optional): A flag indicating whether the resulting time should be returned as an ISO formatted string or as a datetime object. Default is False.
            
        Returns:
            The resulting time as either an ISO formatted string or a datetime object.
        """
        if string:
            return (timezone.now()+delta).isoformat()
        
        return timezone.now() + delta
    

    @classmethod
    def compare(cls, dt: str|datetime, comp: str, dt2: str|datetime=None) -> bool:
        """
        Compares two datetime objects or ISO formatted strings using a specified comparison operator.
        
        Args:
            dt: The first datetime object or ISO formatted string to compare.
            comp: The comparison operator to use. Can be '>', '<', or '='.
            dt2 (optional): The second datetime object or ISO formatted string to compare. If not provided, the current time will be used.
            
        Returns:
            A boolean indicating the result of the comparison.
            
        Raises:
            Exception: If an invalid comparison operator is provided.
        """
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

