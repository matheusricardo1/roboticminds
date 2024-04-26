from .test_api_views_base import APIViewTestBase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse
from django.test import Client
from django.core.files.base import ContentFile 
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
import json
from unittest import skip


class APIViewTest(APIViewTestBase):
    def test_api_view_login(self):
        response = self.register_and_login()
        json_response = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json_response["refresh"], str)
        self.assertIsInstance(json_response["access"], str)


    def test_api_view_register_user_is_working(self):
        response = self.register()

        expected_message = 'Usuário cadastrado com sucesso!'       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_message)

    def test_api_view_register_user_erros_validators_is_working(self):
        createuser = json.dumps(self.make_user())
        response = self.client.post(reverse("api:user_register"), createuser, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        server_request = json.dumps(self.make_user(
            password = '123', 
            email = 'matheus_gmail.com', 
            birth_date = '2006-07-30123',
            level_access = 'studentt', 
            sex = 'MM'
        ))

        response = self.client.post(reverse("api:user_register"), server_request, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

        '''
        expected_message = self.server_all_errors()
        errors = json.loads(response.content.decode('utf-8'))
        username_error = errors['username']
        password_error = errors['password']
        other_fields_error = errors['other_fields']
        birth_date_error = other_fields_error['birth_date']
        expected_keys_error = other_fields_error['level_access_available']['expected_keys']
        expected_keys_error.sort()
        expected_message['other_fields']['level_access_available']['expected_keys'].sort()
        email_error = other_fields_error['email']
        level_access_error = other_fields_error['level_access']
        sex_error = other_fields_error['sex']

        self.assertListEqual(username_error, expected_message['username'])
        self.assertListEqual(password_error, expected_message['password'])
        self.assertEqual(birth_date_error, expected_message['other_fields']['birth_date'])
        self.assertListEqual(expected_keys_error, expected_message['other_fields']['level_access_available']['expected_keys'])
        self.assertEqual(email_error, expected_message['other_fields']['email'])
        self.assertEqual(level_access_error, expected_message['other_fields']['level_access'])
        self.assertEqual(sex_error, expected_message['other_fields']['sex'])
        '''
    @skip('Conflits with the main production files')
    def test_api_view_user_update_is_working(self):
        response = self.register()
        self.assertEqual(response.status_code, 200)

        image = ContentFile(b"foo", "test_image.jpg")
        user_update = {
            "id": 1,
            "username": "matheus",
            "profile_picture": image
        }

        response = self.client.put(
            reverse('api:users'),
            data=encode_multipart(data=user_update, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT
        )
        
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('api:users'),
            json.dumps({
                "id": 1
            }),
            content_type='application/json'
        )
        
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['results'][0]['profile_picture'], '/media/profile_pictures/JPG/matheus_profile_picture.jpg')


        user_update = {
            "id": 1,
            "profile_picture": "delete"
        }

        response = self.client.put(
            reverse('api:users'),
            data=encode_multipart(data=user_update, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT
        )

        response = self.client.post(
            reverse('api:users'),
            json.dumps({
                "id": 1
            }),
            content_type='application/json'
        )
        content = json.loads(response.content.decode('utf-8'))
        print(content['results'][0]['profile_picture'])
        self.assertEqual(content['results'][0]['profile_picture'], '////media/profile_pictures/JPG/matheus_profile_picture.jpg')

        #response = self.client.get('/media/profile_pictures/JPG/matheus_profile_picture.jpg')
        #self.assertEqual(response.status_code, 200)