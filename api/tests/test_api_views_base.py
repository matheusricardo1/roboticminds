from django.test import TestCase
import json

class APIViewTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def make_user_login(self, username = 'matheus12345', password = 'dragonmines123'): 
        return {
            'username': username,
            'password': password
        }

    def make_user(
        self,
        username = 'matheus12345',
        password = 'dragonmines123', 
        email = 'matheusricardo164@gmail.com', 
        cpf = '12345678910', 
        registration = '12345678910', 
        birth_date = '2006-07-30',
        level_access = 'student', 
        sex = 'M'
    ):
        return {
            'username': username,
            'password': password, 
            'email': email, 
            'cpf': cpf, 
            'registration': registration, 
            'birth_date': birth_date,
            'level_access': level_access, 
            'sex': sex
        }

    def server_all_errors(self):
        return {
            "username": [
                "Um usuário com este nome de usuário já existe.",
                "Um usuário com este nome de usuário já existe."
            ],
            "password": [
                "Esta senha é muito curta. Ela precisa conter pelo menos 8 caracteres.",
                "Esta senha é muito comum.",
                "Esta senha é inteiramente numérica."
            ],
            "other_fields": {
                "birth_date": "Formato inválido para data. Use um dos formatos a seguir: YYYY-MM-DD.",
                "level_access_available": {
                    "expected_keys": [
                        "staff",
                        "teacher",
                        "student"
                    ]
                },
                "email": "Insira um endereço de email válido.",
                "level_access": "\"studentt\" não é um escolha válido.",
                "sex": "Certifique-se de que este campo não tenha mais de 1 caracteres."
            },
            "extra_keys": []
        }       