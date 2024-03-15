from django.test import TestCase
from ..models import RoboticUser

class RoboticTestBase(TestCase):
    def setUp(self) -> None:
            return super().setUp()

    def make_user(
        self,
        username = "matheus1",
        first_name = "Matheus",
        last_name = "Ricardo",
        email = "emailtest@gmail.com",
        password = "passwordtest123",
        is_active = True,
        is_staff = False,
        is_superuser  = False,
        full_name = "Matheus Ricardo Oliveira Lima",
        mini_bio = "Me Chamo Matheus",
        cpf = "12345678900",
        registration = "12345678900",
        profile_picture = None,
        birth_date = None,
        level_access = 'Student',
        sex = 'M',
        school = None,
    ):
        return RoboticUser.objects.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password,
            is_active = is_active,
            is_staff = is_staff,
            is_superuser  = is_superuser,
            full_name = full_name,
            mini_bio = mini_bio,
            cpf = cpf,
            registration = registration,
            profile_picture = profile_picture,
            birth_date = birth_date,
            level_access = level_access,
            sex = sex,
            school = school,
        )
