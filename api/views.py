from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from robotic.models import RoboticUser
from api.serializers import RoboticUserSerializer
from .validators import user_validator
from django.contrib.auth.hashers import make_password


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
            return JsonResponse("Usuário cadastrado com sucesso!", safe=False)
        return error(user_serializer.errors)
    
    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        
        user = get_object_or_404(RoboticUser, id=user_data.get('id'))
        user_data['password'] = make_password(user_data['password'])
        user.password = make_password(user.password)
        user.save()
        user_serializer = RoboticUserSerializer(user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Usuário atualizado com sucesso!", safe=False)
        return error(user_serializer.errors)
    
    elif request.method == 'DELETE':
        user = get_object_or_404(RoboticUser, id=id)
        user.delete()
        return JsonResponse("Usuário deletado com sucesso!", safe=False)

@api_view(['POST'])
def user_register(request):
    user_data = JSONParser().parse(request)
    user_validation = user_validator(user_data)
    #user_serializer = RoboticUserSerializer(data=user_data)

    if user_validation.get("errors", False):
        errors = user_validation["errors"]
        return JsonResponse(errors, status=400, safe=False)
    #user_instance = user_serializer.save()

    return JsonResponse("Usuário cadastrado com sucesso!", safe=False)


def error(errors):
    print(f'User Serializer Errors: {errors}')
    return JsonResponse({"errors": errors}, safe=False)
