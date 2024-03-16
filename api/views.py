from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from robotic.models import RoboticUser
from api.serializers import RoboticUserSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
#@permission_classes([IsAuthenticated])
def users(request, id=0):
    if request.method == 'GET':
        users = RoboticUser.objects.all().order_by("-id")
        user_serializer = RoboticUserSerializer(users, many=True)
        return JsonResponse(user_serializer.data, safe=False)

    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer = RoboticUserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Usuário cadastrado com sucesso!", status=201)
        return error(user_serializer.errors)
    
    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        user = get_object_or_404(RoboticUser, id=user_data.get('id'))
        user_serializer = RoboticUserSerializer(user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Usuário atualizado com sucesso!", status=200)
        return error(user_serializer.errors)
    
    elif request.method == 'DELETE':
        user = get_object_or_404(RoboticUser, id=id)
        user.delete()
        return JsonResponse("Usuário deletado com sucesso!", status=204)

def error(errors):
    print(f'User Serializer Errors: {errors}')
    return JsonResponse({"errors": errors}, status=400)
