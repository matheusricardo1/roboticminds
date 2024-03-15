from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
#from robotic.models import Aluno
#from api.serializers import AlunoSerializer


#@csrf_exempt
#def alunos(request):
#    if request.method == 'GET':
#        aluno = Aluno.objects.all().order_by("-id")
#        aluno_serializer = AlunoSerializer(aluno, many=True)
#        return JsonResponse(aluno_serializer.data, safe=False)
#
#
#    elif request.method == 'POST':
#        aluno_data = JSONParser().parse(request)
#        aluno_serializer = AlunoSerializer(data=aluno_data)
#        if aluno_serializer.is_valid():
#            aluno_serializer.save()
#            return JsonResponse("Cadastrado com suscesso!", safe=False)
#        return JsonResponse("Falha ao Cadastrar!", safe=False)
    