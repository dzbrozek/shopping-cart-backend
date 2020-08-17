from baskets.factories import BasketFactory
from django.conf import settings
from django.urls import reverse
from djangorestframework_camel_case.util import camelize
from rest_framework.test import APITestCase
from users.factories import USER_PASSWORD, UserFactory
from users.serializers import MeSerializer
from utils.tests import BasketTestMixin


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


class LoginAPIViewTest(BasketTestMixin, APITestCase):
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

    def test_preserve_basket_during_login(self):
        basket = BasketFactory()

        self.set_up_basket_session(str(basket.uuid))

        data = {'email': self.user.email, 'password': USER_PASSWORD}

        response = self.client.post(reverse('users:login'), data=data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.client.session[settings.BASKET_SESSION_ID], str(basket.uuid))


class LogoutAPIViewTest(BasketTestMixin, APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_log_out(self):
        self.client.force_login(self.user)

        self.assertIn('_auth_user_id', self.client.session)

        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, 204)

        self.assertNotIn('_auth_user_id', self.client.session)

    def test_preserve_basket_during_logout(self):
        self.client.force_login(self.user)
        basket = BasketFactory()

        self.set_up_basket_session(str(basket.uuid))

        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, 204)

        self.assertEqual(self.client.session[settings.BASKET_SESSION_ID], str(basket.uuid))
