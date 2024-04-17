from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from robotic.models import RoboticUser
from api.serializers import RoboticUserSerializer
from datetime import datetime
from django.contrib.auth.hashers import make_password
from random import randint


def check_expected_values(data, errors):
    expected_keys = {'username', 'password', 'email', 'cpf', 'registration', 'birth_date', 'level_access', 'sex', 'profile_picture'}
    extra_keys = []
    for data in data:
        if data not in expected_keys:
            extra_keys.append(f'{data} expected {expected_keys}')

    if len(extra_keys) > 0:
        if "extra_keys" not in errors["errors"]:
            errors["errors"]["extra_keys"] = [] 
        errors["errors"]["extra_keys"].extend(extra_keys)
    return errors

def default_errors():
    errors = {
        "message": "Não foi possível modificar com sucesso!",
        "errors": {
            "username": [],
            "password": [],
            "other_fields": {},
            "extra_keys": []
        },
    }
    return errors

def user_object(user):
    birth_date = user.get('birth_date', None)
    randomic = [False, True, None]
    if birth_date in randomic:
        birth_date = f'{str(randint(2000,2010))}-{str(randint(1,12))}-{str(randint(1,30))}'

    user_obj = {
        "username": user.get('username', None),
        "password": user.get('password', None),
        "email": user.get('email', ''),
        "cpf": user.get('cpf', str(randint(10000000000, 99999999999))),
        "registration": user.get('registration', str(randint(10000000000, 99999999999))),
        "birth_date": birth_date,
        "level_access": user.get('level_access', 'student'),
        "sex": user.get('sex', ''),
        "profile_picture": user.get('profile_picture', None),
    }
    return user_obj

def min_data_expected(user, errors, random_birth_date=False):
    if user['username'] is None:
        errors["errors"]["username"] = f"Não recebido! Username é obrigatório!"

    if user['password'] is None:
        errors["errors"]["password"] = f"Não recebido! Password é obrigatório!"

    error = validate_birth_date(user, errors, random_birth_date=random_birth_date)
    
    return errors

def validate_birth_date(user, errors, random_birth_date=False):
    if user['birth_date'] is None:
        errors["errors"]["other_fields"]["birth_date"] = f"Não recebida! Formato Esperado: YYYY-MM-DD Error"
    else:
        try:
            user['birth_date'] = datetime.strptime(user['birth_date'], "%Y-%m-%d").date()
        except ValueError as e:
           errors["errors"]["other_fields"]["birth_date"] = f"Data inválida! Recebido: {birth_date}, Formato Esperado: YYYY-MM-DD Error"

    return errors

def check_level_access(user, errors):
    expected_keys = {'teacher', 'student', 'staff'}
    if user['level_access'] not in expected_keys:
        errors["errors"]["other_fields"]["level_access_available"] = {
        "expected_keys": list(expected_keys)
    }
    return errors

def check_password(user, errors):
    if user['password'] is None:
        errors["errors"]["password"] = f'Password é obrigatório!'
    else:
        try:
            validate_password(user['password'])
        except ValidationError as e:
            for error in e.messages:
                errors["errors"]["password"].append(error)   
    return errors

def check_all_user_fields(user, errors):
    try:
        user_instance = RoboticUser(
            username=user['username'],
            password=user['password'], 
            email=user['email'],
            cpf=user['cpf'],
            registration=user['registration'],
            birth_date=user['birth_date'],
            level_access=user['level_access'],
            sex=user['sex'],
            profile_picture=user['profile_picture'],
        )
        user_instance.full_clean() 
    except ValidationError as e:
        for field, error in e.message_dict.items():
            if field in ['username', 'password']:
                errors["errors"][field] = error
            else:
                errors["errors"]["other_fields"][field] = error[0]

    return errors

def user_validator(user):
    user = user_object(user)
    errors = default_errors()
    errors = min_data_expected(user, errors, random_birth_date=True)
    errors = check_expected_values(user, errors)
    errors = check_level_access(user, errors)
    errors = check_password(user, errors)
    errors = check_all_user_fields(user, errors)

    if not any(errors["errors"].values()):
        user_instance = RoboticUser.objects.create(
            username=user['username'],
            password=user['password'], 
            email=user['email'],
            cpf=user['cpf'],
            registration=user['registration'],
            birth_date=user['birth_date'],
            level_access=user['level_access'],
            sex=user['sex'],
            profile_picture=user['profile_picture'],
        )
        user_instance.password = make_password(user['password'])
        user_instance.save()
        return {
            "message": "Usuário cadastrado com sucesso!",
        }

    return errors