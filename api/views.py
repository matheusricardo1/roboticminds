from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from robotic.models import RoboticUser
from api.serializers import RoboticUserSerializer
from .validators import user_validator
from django.contrib.auth.hashers import make_password
import json
import base64
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import imghdr
from rest_framework.parsers import MultiPartParser
from django.utils.text import slugify
import os


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
#@permission_classes([IsAuthenticated])
def users(request, id=0):
    if request.method == 'GET':
        users = RoboticUser.objects.all().order_by("-id")
        user_serializer = RoboticUserSerializer(users, many=True)
        return JsonResponse(user_serializer.data, safe=False)

    elif request.method == 'POST':
        data_expected = {'id', 'username', 'email', 'cpf', 'registration', 'birth_date', 'level_access', 'sex', 'is_activated_by_admin'}
        #parser_classes = [MultiPartParser]
        #user_data = request.data
        user_data = JSONParser().parse(request)

        for data in user_data:
            if data not in data_expected:
                return JsonResponse(f"Json tem dados inesperados. É esperado: {data_expected}", safe=False)

        user = RoboticUser.objects.filter(**user_data).order_by("-id")
        if user is not None:
            user_serializer = RoboticUserSerializer(user, many=True)
            return JsonResponse(user_serializer.data, safe=False)
            #return JsonResponse(user_serializer, safe=False)
        else:
            return JsonResponse("Json tem dados indejesados", safe=False)
    
    if request.method == 'PUT':
        data_expected = {'id', 'username', 'password', "email", "cpf", "registration", "birth_date", "level_access", "sex", 'profile_picture', 'full_name', 'mini_bio', 'school', 'is_activated_by_admin'}
        parser_classes = [MultiPartParser]
        user_data = request.data.copy()

        #user_data = JSONParser().parse(request)
        for data in user_data:
            if data not in data_expected:
                return JsonResponse(f"Json tem dados inesperados. É esperado: {data_expected}", safe=False)

        user = get_object_or_404(RoboticUser, id=user_data.get('id'))     
   
        profile_picture = user_data.get('profile_picture', None)

        if profile_picture is not None:
            if user.profile_picture or profile_picture == 'delete':
                if user.profile_picture and os.path.isfile(user.profile_picture.path):
                    try:
                        os.remove(user.profile_picture.path)
                    except Exception as e:
                        print(f"Error removing file: {e}")

                user.profile_picture = None

            if profile_picture != 'delete':
                image = request.FILES.get('profile_picture')
                file_name = image.name
                username = slugify(user.username) 
                        
                ext = os.path.splitext(file_name)[1]    
                ext = ext.replace('.', '')
                file_ext_name = ext.upper() 
                new_filename = f"{file_ext_name}/{username}_profile_picture.{ext}"
                user.profile_picture.upload_to = 'profile_pictures/'
                user.profile_picture.save(new_filename, image)
            user_data.pop('profile_picture', None)
    
        password = user_data.get('password', None)
        if password is not None:
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
