from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view # , permission_classes
# from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from robotic.models import RoboticUser, Certificate, CertificateAssignment, Project, Event, UserProjectAssignment, UserEventAssignment
from api.serializers import RoboticUserSerializer, CertificateSerializer, CertificateAssignmentSerializer, ProjectSerializer, EventSerializer, UserProjectAssignmentSerializer, UserEventAssignmentSerializer
from api.pagination import UserAPIPagination, CertificateAPIPagination
from api.validations import APIRequest, UserValidation, AuthValidation
from .certificate_download import *



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
        user_data = request.data.copy()
        password = user_data.get('password')

        if not password:
            return Response({"password": ["Este campo é obrigatório."]}, status=400)

        user_data['password'] = make_password(password) 

        user_serializer = RoboticUserSerializer(data=user_data)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response("Usuário criado com sucesso!", status=201)
        return Response(user_serializer.errors, status=400)

    def put(self, request, format=None):
        data = request.data.copy()
        try:
            pk = data['id']
            user = RoboticUser.objects.get(pk=pk)
        except RoboticUser.DoesNotExist:
            return Response("Usuário não encontrado", status=404)

        if len(data) == 1:
            return Response("É preciso mais dados além do ID", status=400)

        if 'password' in data:
            data['password'] = make_password(data['password'])

        serializer = RoboticUserSerializer(user, data=data, partial=True)

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
        certificates = CertificateSerializer(data=request.data)
        
        if certificates.is_valid():
            certificates.save()
            return Response("Certificado criado com sucesso!", status=201)
        
        return Response(certificates.errors, status=400)

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
            data = assignment_serializer.validated_data
            user = data.get('user')
            certificate = data.get('certificate')
            try:
                exists = CertificateAssignment.objects.get(user=user.id, certificate=certificate.id)
                return Response("Atribuição não foi realizada com suscesso pois o certificado já está atruido ao usuário!", status=400)
            except CertificateAssignment.DoesNotExist:
                return Response("Atribuição não foi realizada com suscesso!", status=400)

            if user.level_access == "teacher" and not exists:
                return Response("Atribuição não foi realizada com suscesso pois o usuario fornecido é um professor!", status=400)

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


class ProjectAPI(APIView):
    def get(self, request, format=None):
        projects = Project.objects.all().order_by("-start_date")
        if not projects:
            return Response("Nenhum projeto no sistema")
        
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Projeto criado com sucesso!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, format=None):
        data = request.data
        try:
            pk = data['id']
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response("Projeto não encontrado", status=status.HTTP_404_NOT_FOUND)

        if len(data) == 1:
            return Response("É preciso mais dados além do ID", status=status.HTTP_400_BAD_REQUEST)

        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Projeto modificado com sucesso!", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response("Projeto não encontrado", status=status.HTTP_404_NOT_FOUND)

        project.delete()
        return Response("Projeto deletado com sucesso", status=status.HTTP_204_NO_CONTENT)


class EventAPI(APIView):
    def get(self, request, format=None):
        events = Event.objects.all().order_by("-date")
        if not events:
            return Response("Nenhum evento no sistema")
        
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Evento criado com sucesso!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, format=None):
        data = request.data
        try:
            pk = data['id']
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response("Evento não encontrado", status=status.HTTP_404_NOT_FOUND)

        if len(data) == 1:
            return Response("É preciso mais dados além do ID", status=status.HTTP_400_BAD_REQUEST)

        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Evento modificado com sucesso!", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response("Evento não encontrado", status=status.HTTP_404_NOT_FOUND)

        event.delete()
        return Response("Evento deletado com sucesso", status=status.HTTP_204_NO_CONTENT)


class UserProjectAssignmentAPI(APIView):
    def get(self, request, format=None):
        assignments = UserProjectAssignment.objects.all().order_by("-assignment_date")
        if not assignments:
            return Response("Nenhuma atribuição de projeto no sistema")
        
        serializer = UserProjectAssignmentSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = UserProjectAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Atribuição de projeto criada com sucesso!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, format=None):
        data = request.data
        try:
            pk = data['id']
            assignment = UserProjectAssignment.objects.get(pk=pk)
        except UserProjectAssignment.DoesNotExist:
            return Response("Atribuição de projeto não encontrada", status=status.HTTP_404_NOT_FOUND)

        if len(data) == 1:
            return Response("É preciso mais dados além do ID", status=status.HTTP_400_BAD_REQUEST)

        serializer = UserProjectAssignmentSerializer(assignment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Atribuição de projeto modificada com sucesso!", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        try:
            assignment = UserProjectAssignment.objects.get(pk=pk)
        except UserProjectAssignment.DoesNotExist:
            return Response("Atribuição de projeto não encontrada", status=status.HTTP_404_NOT_FOUND)

        assignment.delete()
        return Response("Atribuição de projeto deletada com sucesso", status=status.HTTP_204_NO_CONTENT)


class UserEventAssignmentAPI(APIView):
    def get(self, request, format=None):
        assignments = UserEventAssignment.objects.all().order_by("-assignment_date")
        if not assignments:
            return Response("Nenhuma atribuição de evento no sistema")
        
        serializer = UserEventAssignmentSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = UserEventAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Atribuição de evento criada com sucesso!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, format=None):
        data = request.data
        try:
            pk = data['id']
            assignment = UserEventAssignment.objects.get(pk=pk)
        except UserEventAssignment.DoesNotExist:
            return Response("Atribuição de evento não encontrada", status=status.HTTP_404_NOT_FOUND)

        if len(data) == 1:
            return Response("É preciso mais dados além do ID", status=status.HTTP_400_BAD_REQUEST)

        serializer = UserEventAssignmentSerializer(assignment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Atribuição de evento modificada com sucesso!", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        try:
            assignment = UserEventAssignment.objects.get(pk=pk)
        except UserEventAssignment.DoesNotExist:
            return Response("Atribuição de evento não encontrada", status=status.HTTP_404_NOT_FOUND)

        assignment.delete()
        return Response("Atribuição de evento deletada com sucesso", status=status.HTTP_204_NO_CONTENT)
