from django.urls import reverse
from djangorestframework_camel_case.util import camelize
from rest_framework.test import APITestCase
from users.factories import USER_PASSWORD, UserFactory
from users.serializers import MeSerializer


class MeAPIViewTest(APITestCase):
    def test_authenticated_user_can_get_user_data(self):
        user = UserFactory(is_active=True)
        self.client.force_login(user)

        response = self.client.get(reverse('users:me'))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), camelize(MeSerializer(user).data))

    def test_unauthenticated_user_cannot_get_user_data(self):
        response = self.client.get(reverse('users:me'))

        self.assertEqual(response.status_code, 403)


class LoginAPIViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_active=True)

    def test_log_in(self):
        data = {'email': self.user.email, 'password': USER_PASSWORD}

        response = self.client.post(reverse('users:login'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), camelize(MeSerializer(self.user).data))

        self.assertIn('_auth_user_id', self.client.session)

    def test_invalid_credentials(self):
        data = {'email': 'invalid@email.com', 'password': 'invalid-password'}

        response = self.client.post(reverse('users:login'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'nonFieldErrors': ['Invalid credentials']})


class LogoutAPIViewTest(APITestCase):
    def test_log_out(self):
        user = UserFactory()
        self.client.force_login(user)

        self.assertIn('_auth_user_id', self.client.session)

        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, 204)

        self.assertNotIn('_auth_user_id', self.client.session)
