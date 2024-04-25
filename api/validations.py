from robotic.models import RoboticUser
from django.db import models
from api.validation.base import BaseAuthValidation, BaseRequestValidation,BaseUserValidation


class AuthValidation(BaseAuthValidation):
    def __init__(self, request, random_data=True):
        self.random_data = random_data
        self.request = request
        self.user = request.data
        self.validation()


class APIRequest(BaseRequestValidation):
    def user_register_validation(self):
        self.data_expected = ['id', 'username', 'password', "email", "cpf", "registration", "birth_date", "level_access", "sex", 'profile_picture', 'full_name', 'mini_bio', 'school', 'is_activated_by_admin']
        self.set_unexpect_data_item_null()

    def user_post_validation(self):
        self.data_expected = {'id', 'username', 'email', 'cpf', 'registration', 'birth_date', 'level_access', 'sex', 'is_activated_by_admin'}
        self.set_unexpect_data_item_null()

    def user_put_validation(self):
        self.data_expected = {'id', 'username', 'password', "email", "cpf", "registration", "birth_date", "level_access", "sex", 'profile_picture', 'full_name', 'mini_bio', 'school', 'is_activated_by_admin'}
        self.set_unexpect_data_item_null()

    def __init__(self, request):
        self.request = request
        if "register" in self.request.path:
            if self.request.method == "POST":
                self.user_register_validation()
        else:
            if self.request.method == 'POST':
                self.user_post_validation()
            if self.request.method == 'PUT':
                self.user_put_validation()
    

class UserValidation(BaseUserValidation):
    def filter_users_by_data(self):
        self.error = 'Nenhum usuário encontrado'
        query_filters = {}
        char_fields = []
        unique_fields = []
        choices_fields = []
        exception_fields = []

        for field in RoboticUser._meta.fields:
            if isinstance(field, models.fields.CharField):
                char_fields.append(field.name)
            if field.choices:
                choices_fields.append(field.name)
            if field.unique and field.name not in exception_fields:
                unique_fields.append(field.name)

        for (key, value) in self.data.items():
            if key in char_fields and key not in unique_fields and key not in choices_fields:
                query_filters[f'{key}__icontains'] = value
            else:
                query_filters[key] = value
                
        self.users = RoboticUser.objects.filter(**query_filters).order_by("-id")  

    def update_user_by_data(self):
        self.data_expected = APIRequest(self.request).data_expected
        self.user_id = self.data.get('id', None)

        if self.user_id is None:
            self.error = f'Id é Obrigatório, é esperado: {self.data_expected}'
            self.valid = False
            

        try:
            self.user = RoboticUser.objects.get(id=self.user_id)
        except Exception as e:
            self.error = f'Usuário não encontrado!'
            self.valid = False
            
        
        if len(self.data) == 1:
            self.error = f"Id do usuário foi fornecido, mas não foi fornecido os campos e seus respectivos novos valores, é esperado: {self.data_expected}"
            self.valid = False
            

        self.picture_manager()
        self.change_password()

    def __init__(self, request):
        self.request = request
        self.data = request.data

        if self.request.method == "POST":
            self.filter_users_by_data()
        if self.request.method == "PUT":
            self.update_user_by_data()

        self.check_is_robotic_user()


