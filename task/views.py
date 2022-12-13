from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist


from account.decorators import authenticated
from .models import Task
from .serializers import TaskSerializer
from .exception import InvalidOwnership


@api_view(['POST'])
@authenticated
def create_task(req, *args, **kwargs):
    try:
        serializer = TaskSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save(user_id=req.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except: 
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


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
    except ObjectDoesNotExist:
        return Response({'message': 'task not found'}, status=status.HTTP_404_NOT_FOUND)
    except: 
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authenticated
def list_tasks(req, *args, **kwargs):
    try:
        tasks = Task.objects.filter(user_id=req.user.id)
        data = TaskSerializer(tasks, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    except: 
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@authenticated
def update_task(req, task_id, *args, **kwargs):
    try:
        task = Task.objects.get(id=task_id, user_id=req.user.id)
        ser = TaskSerializer(task, data=req.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({'message': 'task not found'}, status=status.HTTP_404_NOT_FOUND)
    except: 
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@authenticated
def delete_task(req, task_id, *args, **kwargs):
    try:
        task = Task.objects.get(id=task_id, user_id=req.user.id)
        task.delete()
        return Response(status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'message': 'task not found'}, status=status.HTTP_404_NOT_FOUND)
    except: 
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@authenticated
def delete_completed_tasks(req, *args, **kwargs):
    try:
        tasks = Task.objects.filter(user_id=req.user.id, completed=True)
        i, _ = tasks.delete()
        return Response({"deleted_tasks": i}, status=status.HTTP_200_OK)
    except: 
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@authenticated
def delete_tasks(req, *args, **kwargs):
    try:
        tasks = Task.objects.filter(user_id=req.user.id)
        i, _ = tasks.delete()
        return Response({"deleted_tasks": i}, status=status.HTTP_200_OK)
    except: 
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)