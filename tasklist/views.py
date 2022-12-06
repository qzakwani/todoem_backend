from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


# ! implement celery to handle listtasks

@api_view(['POST'])
def create_tasklist(req, *args, **kwargs):
    try:
        pass
    except:
        pass