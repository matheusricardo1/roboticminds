from django.test import TestCase
from ..models import RoboticUser
from .test_robotic_models_base import RoboticTestBase
from django.contrib.auth import authenticate, login, logout


class RoboticModelsTest(RoboticTestBase):

    def test_robotic_models_user_is_created_correct(self):
        username = 'username_test'
        user = self.make_user(username=username)
        self.assertIs(1, user.id)
        self.assertIs(username, user.username)
        self.assertIs(True, user.is_active)
        #self.assertIs(1,1)

    def test_robotic_models_user_is_logging_correct(self):
        username = 'username_test'
        password = 'password_test'
        user = self.make_user(username=username, password=password)
        auth_user = authenticate(username=username, password=password)

        self.assertIsNotNone(auth_user)
        self.assertIsNotNone(auth_user.id)
        self.assertIsNotNone(auth_user.username)
