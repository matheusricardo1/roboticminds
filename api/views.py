import os
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework.decorators import api_view # , permission_classes
# from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser # , MultiPartParser
from api.serializers import RoboticUserSerializer
from robotic.models import RoboticUser
from .validators import user_validator
from .pagination import UserAPIPagination


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
#@permission_classes([IsAuthenticated])
def users(request, id=0):
    if request.method == 'GET':
        list_users = RoboticUser.objects.all().order_by("-id")
        if list_users.count() == 0:
            return JsonResponse("Nenhum usuário no sistema", safe=False)
        paginator = UserAPIPagination()
        result_page = paginator.paginate_queryset(list_users, request)
        user_serializer = RoboticUserSerializer(result_page, many=True)
        return paginator.get_paginated_response(user_serializer.data)

    if request.method == 'POST':
        data_expected = {'id', 'username', 'email', 'cpf', 'registration', 'birth_date', 'level_access', 'sex', 'is_activated_by_admin'}
        user_data = JSONParser().parse(request)

        for data in user_data:
            if data not in data_expected:
                return JsonResponse(f"Json tem dados inesperados. É esperado: {data_expected}", safe=False, status=400)
        list_users = RoboticUser.objects.filter(**user_data).order_by("-id") 
        paginator = UserAPIPagination()

        if list_users is None:
            return JsonResponse("Json tem dados indejesados", safe=False, status=400)
        if list_users.count() == 0:
            return JsonResponse("Nenhum usuário encontrado", safe=False, status=404)
        
        result_page = paginator.paginate_queryset(list_users, request)
        user_serializer = RoboticUserSerializer(result_page, many=True)
        return paginator.get_paginated_response(user_serializer.data)

    if request.method == 'PUT':
        data_expected = {'id', 'username', 'password', "email", "cpf", "registration", "birth_date", "level_access", "sex", 'profile_picture', 'full_name', 'mini_bio', 'school', 'is_activated_by_admin'}
        # parser_classes = [MultiPartParser]
        user_data = request.data.copy()
        user_id = user_data.get('id', None)
        
        if user_id is None:
            return JsonResponse(f"Id é Obrigatório, é esperado: {data_expected}", safe=False, status=400)
        try:
            user = RoboticUser.objects.get(id=user_id)
        except Exception as e:
            return JsonResponse("Usuário não encontrado!", safe=False, status=404)

        if len(user_data) == 1:
            return JsonResponse(f"Id do usuário foi fornecido, mas não foi fornecido os campos e seus respectivos novos valores, é esperado: {data_expected}", safe=False, status=400)

        for data in user_data:
            if data not in data_expected:
                return JsonResponse(f"Json tem dados inesperados. É esperado: {data_expected}", safe=False, status=400)

        profile_picture = user_data.get('profile_picture', None)

        if profile_picture is not None:
            if user.profile_picture or profile_picture == 'delete':
                if user.profile_picture and os.path.isfile(user.profile_picture.path):
                    try:
                        os.remove(user.profile_picture.path)
                    except FileNotFoundError as e:
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
        try:
            user = RoboticUser.objects.get(id=id)
            user.delete()
        except Exception as e:
            if id == 0:
                return JsonResponse("ID é esperado via endpoint, ex: (/users/<id>/)", safe=False, status=400)
            return JsonResponse("Usuário não encontrado!", safe=False, status=404)
        return JsonResponse("Usuário deletado com sucesso!", safe=False)


@api_view(['POST'])
def user_register(request):
    data_expected = {'id', 'username', 'password', "email", "cpf", "registration", "birth_date", "level_access", "sex", 'profile_picture', 'full_name', 'mini_bio', 'school', 'is_activated_by_admin'}
    # parser_classes = [MultiPartParser]
    user_data = request.data.copy()

    for data in user_data:
        if data not in data_expected:
            return JsonResponse(f"[{data}] Não Esperado. É esperado: {data_expected}", safe=False)

    user_validation = user_validator(user_data)

    if user_validation.get("errors", False):
        errors = user_validation["errors"]
        return JsonResponse(errors, status=400, safe=False)

    return JsonResponse("Usuário cadastrado com sucesso!", safe=False)


def error(errors):
    print(f'User Serializer Errors: {errors}')
    return JsonResponse({"errors": errors}, safe=False)
