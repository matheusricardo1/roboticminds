from django.test import TestCase
from ..models import RoboticUser

class TestRoboticModels(TestCase):

    def test_robotic_models_is_created(self):
        username = 'username_test'
        password = 'password_test'
        user = RoboticUser.objects.create_user(username=username, password=password)
        self.assertIs(1, user.id)
        self.assertIs(True, user.is_active)
        #self.assertIs(1,1)
