from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from robotic.models import RoboticUser
from api.serializers import RoboticUserSerializer
from datetime import datetime
from django.contrib.auth.hashers import make_password

def check_expected_values(data, expected_keys, errors):
    #errors["errors"]["other_fields"] = "Check Expect Values: O valor DATA (DATA, expected_keys, errors) deve ser um dicionário"
    extra_keys = []
    for data in data:
        if data not in expected_keys:
            extra_keys.append(f'{data} expected {expected_keys}')

    if len(extra_keys) > 0:
        if "extra_keys" not in errors["errors"]:
            errors["errors"]["extra_keys"] = [] 
        errors["errors"]["extra_keys"].extend(extra_keys)
    return errors
    

def user_validator(user):
    username = user.get('username', None) 
    password = user.get('password', None) 
    email = user.get('email', '') 
    cpf = user.get('cpf', '')
    registration = user.get('registration', '')
    birth_date = user.get('birth_date', None)
    level_access = user.get('level_access', 'student')
    sex = user.get('sex', '')

    errors = {
        "message": "Não foi possível modificar com sucesso!",
        "errors": {
            "username": [],
            "password": [],
            "other_fields": {},
            "extra_keys": []
        },
    }

    if birth_date is not None:
        try:
            birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
            # print(data.year-data.month-data.day)  # Saída: YYYY-MM-DD

        except ValueError as e:
           errors["errors"]["other_fields"]["birth_date"] = f"Data inválida! Recebido: {birth_date}, Formato Esperado: YYYY-MM-DD Error: {e}"

    expected_keys = {'username', 'password', 'email', 'cpf', 'registration', 'birth_date', 'level_access', 'sex'}
    errors = check_expected_values(user, expected_keys, errors)

    expected_keys = {'teacher', 'student', 'staff'}
    if level_access not in expected_keys:
        errors["errors"]["other_fields"]["level_access_available"] = {
        "expected_keys": list(expected_keys)
    }

    try:
        validate_password(password)
    except ValidationError as e:
        for error in e.messages:
            errors["errors"]["password"].append(error)
    try:
        user_instance = RoboticUser(
            username=username,
            password=password, 
            email=email,
            cpf=cpf,
            registration=registration,
            birth_date=birth_date,
            level_access=level_access,
            sex=sex
        )
        user_instance.full_clean() 

    except ValidationError as e:
        for field, error in e.message_dict.items():
            if field in ['username', 'password']:
                errors["errors"][field].extend(error)
            else:
                errors["errors"]["other_fields"][field] = error[0]

    user_serializer = RoboticUserSerializer(data=user)
    if not user_serializer.is_valid():
        for field, error in user_serializer.errors.items():
            if field == 'username' or field == 'password':
                errors["errors"][field].extend(error)
            else:
                errors["errors"]["other_fields"][field] = error[0]
  
    if not any(errors["errors"].values()):
        #user_serializer.save()
        user_instance = RoboticUser.objects.create(
            username=username,
            password=password, 
            email=email,
            cpf=cpf,
            registration=registration,
            birth_date=birth_date,
            level_access=level_access,
            sex=sex
        )
        user_instance.password = make_password(password)
        user_instance.save()
        return {
            "message": "Usuário cadastrado com sucesso!",
        }

    print(f'\nErros de Validação: {errors}\n\n')
    return errors
