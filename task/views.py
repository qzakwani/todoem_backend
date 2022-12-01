from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist


from account.decorators import authenticated
from .models import Task
from .serializers import TaskSerializer
from .exception import InvalidOwnership


@api_view(['GET'])
@authenticated
def get_task(req, task_id, *args, **kwargs):
    try:
        task = Task.objects.get(id=task_id)
        if not task.user_id == req.user.id: raise InvalidOwnership('invalid task ownership')
        data = TaskSerializer(task).data
        return Response(data, status=status.HTTP_200_OK)
    except InvalidOwnership as e:
        return Response({'message': e.args[0]}, status=status.HTTP_403_FORBIDDEN)
    except ObjectDoesNotExist as err:
        return Response({'message': 'task not found'}, status=status.HTTP_404_NOT_FOUND)
    except: 
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        