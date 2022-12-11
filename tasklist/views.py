from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view




@api_view(['POST'])
def create_tasklist(req, *args, **kwargs):
    try:
        print(req.data)
        return Response(status=status.HTTP_200_OK)
    except:
        pass
    
