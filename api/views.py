from rest_framework.decorators import api_view # , permission_classes
# from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from robotic.models import RoboticUser, Certificate, CertificateAssignment
from api.serializers import RoboticUserSerializer, CertificateSerializer, CertificateAssignmentSerializer
from api.pagination import UserAPIPagination, CertificateAPIPagination
from api.validations import APIRequest, UserValidation, AuthValidation

from .certificate_download import *


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
        data = user.get_data()
        user = user.get_user()

        user_serializer = RoboticUserSerializer(user, data=data, partial=True)
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response("Usuário atualizado com sucesso!")
        return Response(user_serializer.errors)

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


class UserAuth(APIView):
    def post(self, request, format=None):
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


class UsersAPI(APIView):
    def get(self, request, format=None):
        list_users = RoboticUser.objects.all().order_by("-id")
  
        if list_users.count() == 0:
            return Response("Nenhum usuário no sistema")

        paginator = UserAPIPagination()
        result_page = paginator.paginate_queryset(list_users, request)
        user_serializer = RoboticUserSerializer(result_page, many=True)
        return paginator.get_paginated_response(user_serializer.data)   

    def post(self, request, format=None):
        user = RoboticUserSerializer(data=request.data)
        
        if user.is_valid():
            user.save()
            return Response("Usuário criado com sucesso!", status=201)
        return Response(user.errors, status=400)

    def put(self, request, format=None):
        data = request.data
        try:
            pk = data['id']
            user = RoboticUser.objects.get(pk=pk)
        except RoboticUser.DoesNotExist:
            return Response("Usuário não encontrado", status=404)

        if len(data) == 1:
            return Response("É preciso mais dados além do ID", status=400)

        serializer = RoboticUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response("Usuário modificado com sucesso!", status=200)

        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            user = RoboticUser.objects.get(id=id)
            user.delete()
        except Exception as e:
            if id == 0:
                return Response("ID é esperado via endpoint, ex: (/users/<id>/)", status=400)
            return Response("Usuário não encontrado!", status=404)
        return Response("Usuário deletado com sucesso!")


class UsersFilterAPI(APIView):
    def post(self, request, format=None):
        data = request.data
        filters = {}

        if 'id' in data:
            filters['id'] = data['id']
        if 'full_name' in data:
            filters['full_name__icontains'] = data['full_name']
        if 'mini_bio' in data:
            filters['mini_bio__icontains'] = data['mini_bio']
        if 'cpf' in data:
            filters['cpf__icontains'] = data['cpf']
        if 'registration' in data:
            filters['registration__icontains'] = data['registration']
        if 'birth_date' in data:
            filters['birth_date__icontains'] = data['birth_date']
        if 'level_access' in data:
            filters['level_access__icontains'] = data['level_access']
        if 'is_activated_by_admin' in data:
            filters['is_activated_by_admin'] = data['is_activated_by_admin']

        users = RoboticUser.objects.filter(**filters)
        paginator = UserAPIPagination()
        result_page = paginator.paginate_queryset(users, request)
        user_serializer = RoboticUserSerializer(result_page, many=True)
        return paginator.get_paginated_response(user_serializer.data)   


class CertificateAPI(APIView):
    def get(self, request, format=None):
        list_certificates = Certificate.objects.all().order_by("-date")
  
        if list_certificates.count() == 0:
            return Response("Nenhum certificado no sistema")

        paginator = CertificateAPIPagination()
        result_page = paginator.paginate_queryset(list_certificates, request)
        certificate_serializer = CertificateSerializer(result_page, many=True)
        return paginator.get_paginated_response(certificate_serializer.data)   

    def post(self, request, format=None):
        certicates = CertificateSerializer(data=request.data)
        
        if certicates.is_valid():
            certicates.save()
            return Response("Certificado criado com sucesso!", status=201)
        
        return Response(certicates.errors, status=400)

    def put(self, request, format=None):
        data = request.data
        try:
            pk = data['id']
            certificate = Certificate.objects.get(pk=pk)
        except Exception as e:
            return Response("Certificado não encontrado", status=404)

        if len(data) == 1:
            return Response("É preciso mais dados além do ID", status=400)

        serializer = CertificateSerializer(certificate, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response("Certificado modificado com sucesso!", status=200)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        try:
            certificate = Certificate.objects.get(pk=pk)
        except Certificate.DoesNotExist:
            return Response("Certificado não encontrado", status=404)

        certificate.delete()
        return Response("Certificado deletado com sucesso", status=204)


class CertificateFilterAPI(APIView):
    def post(self, request, format=None):
        data = request.data
        filters = {}

        if 'name' in data:
            filters['name__icontains'] = data['name']
        if 'city' in data:
            filters['city__icontains'] = data['city']
        if 'id' in data:
            filters['id'] = data['id']
        print(data, filters)

        certificates = Certificate.objects.filter(**filters)
        serializer = CertificateSerializer(certificates, many=True, partial=True)
        return Response(serializer.data, status=200)
    

class CertificateAssignmentAPI(APIView):
    def get(self, request, format=None):
        assignments = CertificateAssignment.objects.all().order_by("-assignment_date")
  
        if assignments.count() == 0:
            return Response("Nenhuma atribuição no sistema")

        paginator = CertificateAPIPagination()
        result_page = paginator.paginate_queryset(assignments, request)
        assignment_serializer = CertificateAssignmentSerializer(result_page, many=True)
        return paginator.get_paginated_response(assignment_serializer.data)   

    def post(self, request, format=None):
        assignment_serializer = CertificateAssignmentSerializer(data=request.data)
        
        if assignment_serializer.is_valid():
            assignment_serializer.save()
            return Response("Atribuição criada com sucesso!", status=201)
        
        return Response(assignment_serializer.errors, status=400)

    def put(self, request, format=None):
        data = request.data
        try:
            pk = data['id']
            assignment = CertificateAssignment.objects.get(pk=pk)
        except CertificateAssignment.DoesNotExist:
            return Response("Atribuição não encontrada", status=404)

        if len(data) == 1:
            return Response("É preciso mais dados além do ID", status=400)

        serializer = CertificateAssignmentSerializer(assignment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response("Atribuição modificada com sucesso!", status=200)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        try:
            assignment = CertificateAssignment.objects.get(pk=pk)
        except CertificateAssignment.DoesNotExist:
            return Response("Atribuição não encontrada", status=404)

        assignment.delete()
        return Response("Atribuição deletada com sucesso", status=204)


class CertificateAssignmentFilterAPI(APIView):
    def post(self, request, format=None):
        data = request.data
        filters = Q()

        if 'user_id' in data:
            filters &= Q(user__id=data['user_id'])
        if 'certificate_id' in data:
            filters &= Q(certificate__id=data['certificate_id'])
        if 'key' in data:
            filters &= Q(key__icontains=data['key'])
        if 'assignment_date' in data:
            filters &= Q(assignment_date=data['assignment_date'])

        assignments = CertificateAssignment.objects.filter(filters).order_by('-assignment_date')
        
        if assignments.count() == 0:
            return Response("Nenhuma atribuição encontrada")

        paginator = CertificateAPIPagination()
        result_page = paginator.paginate_queryset(assignments, request)
        assignment_serializer = CertificateAssignmentSerializer(result_page, many=True)
        return paginator.get_paginated_response(assignment_serializer.data)


class ValidateCertificateAPI(APIView):
    def post(self, request, format=None):
        key = request.data.get('key')
        if not key:
            return Response({"error": "A chave é necessária."}, status=400)
        
        try:
            assignment = CertificateAssignment.objects.get(key=key)
            user = assignment.user
            certificate = assignment.certificate
            response_data = {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "full_name": user.full_name,
                    "cpf": user.cpf,
                },
                "certificate": {
                    "id": certificate.id,
                    "name": certificate.name,
                    "details": certificate.details,
                    "start_date": certificate.start_date,
                    "end_date": certificate.end_date,
                    "city": certificate.city,
                    "hours": certificate.hours,
                }
            }
            return Response(response_data, status=200)
        except CertificateAssignment.DoesNotExist:
            return Response({"error": "Certificado não encontrado."}, status=404)



def download_certificate(request, user_id):
    user_data = get_user_data(user_id)
    
    image_buffer = create_certificate_image()
    pdf_buffer = create_certificate_pdf(image_buffer)
    
    response = FileResponse(pdf_buffer, as_attachment=True, filename='certificate.pdf')
    return response
