from rest_framework.decorators import api_view # , permission_classes
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from robotic.models import RoboticUser
from api.serializers import RoboticUserSerializer
from api.pagination import UserAPIPagination
from api.validations import APIRequest, UserValidation, AuthValidation


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
#@permission_classes([IsAuthenticated])
def users(request, id=0):
    if request.method == 'GET':
        list_users = RoboticUser.objects.all().order_by("-id")
  
        if list_users.count() == 0:
            return Response("Nenhum usuário no sistema")

        paginator = UserAPIPagination()
        result_page = paginator.paginate_queryset(list_users, request)
        user_serializer = RoboticUserSerializer(result_page, many=True)
        return paginator.get_paginated_response(user_serializer.data)

    if request.method == 'POST':
        _request = APIRequest(request)
        if _request.is_not_correct():
            return Response(_request.get_unexpected_data_error())

        list_users = UserValidation(request)
        if list_users.is_not_valid():
            return Response(list_users.get_error())

        paginator = UserAPIPagination()
        result_page = paginator.paginate_queryset(list_users.get_users(), request)
        serializer = RoboticUserSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    if request.method == 'PUT':
        _request = APIRequest(request)
        if _request.is_not_correct():
            return Response(_request.get_unexpected_data_error())

        user = UserValidation(request)
        if user.is_not_valid():
            return Response(user.get_error())

        user = user.get_user()
        user_serializer = RoboticUserSerializer(user, data=request.data, partial=True)
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response("Usuário atualizado com sucesso!")
        return error(user_serializer.errors)

    if request.method == 'DELETE':
        try:
            user = RoboticUser.objects.get(id=id)
            user.delete()
        except Exception as e:
            if id == 0:
                return Response("ID é esperado via endpoint, ex: (/users/<id>/)", status=400)
            return Response("Usuário não encontrado!", status=404)
        return Response("Usuário deletado com sucesso!")


@api_view(['POST'])
def user_register(request):
    _request = APIRequest(request)
    if _request.is_not_correct():
        error = _request.get_unexpected_data_error()
        return Response(error)

    user = AuthValidation(request)

    if user.is_not_valid():
        return Response(user.get_errors())
    
    user.register()
    if user.user_is_registed():
        return Response('Usuário cadastrado com sucesso!')
    return Response('Erro ao cadastrar!')
