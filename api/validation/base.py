import os
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from robotic.models import RoboticUser
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password
from random import randint
from django.db import models


class BaseAuthValidation:
    valid = None
    user_instance = None
    errors = {
        "message": "Não foi possível modificar com sucesso!",
        "errors": {
            "username": [],
            "password": [],
            "other_fields": {},
            "extra_keys": []
        },
    }

    def generate_random_data(self):
        return str(randint(10000000000, 99999999999))

    def get_user_by_data(self):
        self.username = self.user.get('username', None)
        self.password = self.user.get('password', None)
        self.email = self.user.get('email', '')
        self.cpf = self.user.get('cpf', self.generate_random_data())
        self.registration = self.user.get('registration', self.generate_random_data())
        self.birth_date = self.user.get('birth_date', None)
        
        randomic = [False, True, None]
        if self.random_data and self.birth_date in randomic:
            self.birth_date = f'{str(randint(2000,2010))}-{str(randint(1,12))}-{str(randint(1,30))}'

        self.level_access = self.user.get('level_access', 'student')
        self.sex = self.user.get('sex', '')
        self.profile_picture = self.user.get('profile_picture', None)
        self.refresh_user()

    def refresh_user(self):
        self.user = {
            "username": self.username,
            "password":  self.password,
            "email":  self.email,
            "cpf":  self.cpf,
            "registration":  self.registration,
            "birth_date":  self.birth_date,
            "level_access":  self.level_access,
            "sex":  self.sex,
            "profile_picture":  self.profile_picture,
        }

    def check_data_keys(self):
        expected_keys = {'username', 'password', 'email', 'cpf', 'registration', 'birth_date', 'level_access', 'sex', 'profile_picture'}

        extra_keys = []
        for data in self.user:
            if data not in expected_keys:
                extra_keys.append(f'{data} expected {expected_keys}')
                self.valid = False

        if len(extra_keys) > 0:
            if "extra_keys" not in errors["errors"]:
                errors["errors"]["extra_keys"] = [] 
            errors["errors"]["extra_keys"].extend(extra_keys)
            self.valid = False

    def username_error(self):
        if self.username is None:
            self.errors["errors"]["username"] = f"Não recebido! Username é obrigatório!"
            self.valid = False

    def password_error(self):
        if self.password is None:
            errors["errors"]["password"] = f"Não recebido! Password é obrigatório!"
            self.valid = False
        else:
            try:
                validate_password(self.password)
            except ValidationError as e:
                for error in e.messages:
                    errors["errors"]["password"].append(error)  
                self.valid = False

    def level_access_error(self):
        expected_keys = {'teacher', 'student', 'staff'}
        if self.level_access not in expected_keys:
            self.errors["errors"]["other_fields"]["level_access_available"] = {
                "expected_keys": list(expected_keys)
            }
            self.valid = False

    def check_all_fields(self): 
        try:
            user_instance = RoboticUser(**self.user)
            user_instance.full_clean() 
            self.valid = True
        except ValidationError as e:
            self.valid = False
            for field, error in e.message_dict.items():
                if field in ['username', 'password']:
                    self.errors["errors"][field] = error
                else:
                    self.errors["errors"]["other_fields"][field] = error[0]
        
        print(self.errors, self.valid)

    def validation(self):
        self.get_user_by_data()
        self.check_data_keys()
        self.username_error()
        self.password_error()
        self.level_access_error()
        self.check_all_fields()

    def get_errors(self):
        if self.valid == False:
            return self.errors

    def is_valid(self):
        for key, value in self.errors['errors'].items():
            if len(value) != 0:
                self.valid = False
                return self.valid
        self.valid = True
        return self.valid 

    def is_not_valid(self):
        if self.valid is None:
            self.is_valid()
        return not self.valid

    def register(self):
        if self.valid is None:
            self.is_valid()
        if self.valid == True:
            try:
                self.user_instance = RoboticUser.objects.create(**self.user)
                self.user_instance.password = make_password(self.password)
                self.user_instance.save()
            except Exception as e:
                self.valid = False

    def user_is_registed(self):
        if self.valid == True and isinstance(self.user_instance, RoboticUser):
            return True
        return False

    def get_user(self):
        if user_is_registed():
            return self.user_instance


class BaseRequestValidation:
    valid = None

    def is_correct(self):
        data = self.request.data
        self.valid = True

        for data in data:
            if data not in self.data_expected:
                self.valid = False
                self.unexpect_data_item.append(data)

        self.level_access_error_string = ''

        #if data.get('level_access', None) is not None and data.get('level_access', None) not in ('teacher', 'student', 'staff'):
        #    self.level_access_error_string = "level_access deve receber ('teacher', 'student', 'staff')"

        return self.valid
                
    def is_not_correct(self):
        if self.valid == None:
            self.is_correct()
        return not self.valid

    def get_unexpected_data(self):
        if self.unexpect_data_item and self.data_expected:
            return self.unexpect_data_item, self.data_expected
        
    def get_unexpected_data_error(self):
        if self.unexpect_data_item and self.data_expected:
            error_string = f'Os campos esperados são: {self.data_expected}'
            level_access_error_string = ''
            if len(self.unexpect_data_item) < 2:
                return f'O campo: {self.unexpect_data_item}, não é esperado. {error_string}' + level_access_error_string
            return f'Os campos: {self.unexpect_data_item}, não são esperados. {error_string}' + level_access_error_string
    
    def set_unexpect_data_item_null(self):
        self.unexpect_data_item = []


class BaseUserValidation:
    valid = None
    users = None 
    user = None
    error = 'Empty Error'

    def check_is_robotic_user(self):
        if isinstance(self.users, models.QuerySet) or isinstance(self.user, RoboticUser):
            self.valid = True
        else:
            self.valid = False
        return self.valid

    def get_users(self):
        if self.valid:
            return self.users
        return None

    def get_user(self):
        if self.valid:
            return self.user
        return None
    
    def get_data(self):
        if self.valid:
            return self.data
        return None

    def is_valid(self):
        if self.valid == None:
            self.check_is_robotic_user()
        if self.valid == False:
            return False
        return True
        
    def is_not_valid(self):
        if self.valid == None:
            self.is_valid()
        return not self.valid
    
    def get_error(self):
        if self.valid == False:
            return self.error

    def picture_manager(self):
        self.valid = True
        
        profile_picture = self.data.get('profile_picture', None)
        #print(profile_picture)

        if profile_picture is not None:
            try:
                if self.user.profile_picture or profile_picture == 'delete':
                    if profile_picture == 'delete' and os.path.isfile(self.user.profile_picture.path):
                        try:
                            os.remove(self.user.profile_picture.path)
                        except FileNotFoundError as e:
                            self.valid = False
                            print(f"Error removing file: {e}")
                    
                    self.data.pop('profile_picture', None)
                    self.user.save()

                if profile_picture != 'delete':
                    image = self.request.FILES.get('profile_picture')
                    file_name = image.name
                    username = slugify(self.user.username)

                    ext = os.path.splitext(file_name)[1]
                    ext = ext.replace('.', '')
                    file_ext_name = ext.upper()
                    new_filename = f"{file_ext_name}/{username}_profile_picture.{ext}"
                    #self.user.profile_picture.upload_to = 'profile_pictures/'
                    self.user.profile_picture.save(new_filename, image)
                self.data.pop('profile_picture', None)
            except Exception as e:
                self.valid = False
        

    def change_password(self):
        self.valid = True
        password = self.data.get('password', None)
        if password is not None:
            try:
                self.data['password'] = make_password(self.data['password'])
                self.user.password = make_password(self.user.password)
                self.user.save()
            except Exception as e:
                self.valid = False
         

