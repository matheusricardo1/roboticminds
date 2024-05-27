from django.test import TestCase, Client
from django.shortcuts import reverse
import base64
import os
import json


class APIViewTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def register(self, user=None):
        user_register = user
        if user is None:
            user_register = self.make_user()

        return self.client.post(
            reverse("api:users"),
            user_register,
            content_type='application/json'
        )
    
    def login(self, user=None):
        user_login = user
        if user is None:
            user_login = self.make_user_login()
        print(user_login)
        return self.client.post(
            reverse('api:get_token'), 
            user_login, 
            content_type='application/json'
        )

    def register_and_login(self, user=None):
        self.register(user)
        if user is not None:
            user = {
                'username': user.get('username', None),
                'password': user.get('password', None)
            }
        return self.login(user)

    def build_multipart_form_data(self, data, boundary):
        """
        Constrói o conteúdo da solicitação multipart/form-data a partir dos dados fornecidos.
        """
        lines = []
        for key, value in data.items():
            lines.append(f'--{boundary}')
            if isinstance(value, str):
                lines.append(f'Content-Disposition: form-data; name="{key}"')
                lines.append('')
                lines.append(value)
            elif isinstance(value, bytes):
                lines.append(f'Content-Disposition: form-data; name="{key}"; filename="{os.path.basename(value.name)}"')
                lines.append('Content-Type: image/jpeg')
                lines.append('')
                lines.append(value.read())
            else:
                raise ValueError(f'Unsupported data type for key {key}: {type(value)}')
        
        lines.append(f'--{boundary}--')
        lines.append('')
        return '\r\n'.join(str(line) for line in lines)

    def image(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, 'test_image.jpg')

        # Verifique se o arquivo existe
        if os.path.exists(image_path):
            with open(image_path, 'rb') as image_file:
                image_content = image_file.read()
                return image_content
        else:
            print("Arquivo de imagem não encontrado:", image_path)
                


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