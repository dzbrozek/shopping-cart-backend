from unittest import mock

from django.test import RequestFactory, TestCase
from rest_framework.exceptions import ErrorDetail
from users.factories import USER_PASSWORD, UserFactory
from users.serializers import LoginSerializer


class LoginSerializerTest(TestCase):
    def test_missing_data(self):
        data = {
            'email': '',
            'password': '',
        }
        serializer = LoginSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertDictEqual(
            serializer.errors,
            {
                'email': [ErrorDetail(string='This field may not be blank.', code='blank')],
                'password': [ErrorDetail(string='This field may not be blank.', code='blank')],
            },
        )

    def test_invalid_data(self):
        data = {
            'email': 'email',
            'password': 'password',
        }
        serializer = LoginSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertDictEqual(
            serializer.errors, {'email': [ErrorDetail(string='Enter a valid email address.', code='invalid')]}
        )

    def test_invalid_credentials(self):
        data = {
            'email': 'invalid@email.com',
            'password': 'invalid',
        }
        serializer = LoginSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertDictEqual(
            serializer.errors, {'non_field_errors': [ErrorDetail(string='Invalid credentials', code='invalid')]}
        )

    def test_inactive_user(self):
        user = UserFactory(is_active=False)
        data = {
            'email': user.email,
            'password': USER_PASSWORD,
        }
        serializer = LoginSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertDictEqual(
            serializer.errors, {'non_field_errors': [ErrorDetail(string='Invalid credentials', code='invalid')]}
        )

    @mock.patch('users.serializers.login')
    def test_valid_data(self, login_mock):
        user = UserFactory(is_active=True)
        data = {
            'email': user.email,
            'password': USER_PASSWORD,
        }
        context = dict(request=RequestFactory())
        serializer = LoginSerializer(data=data, context=context)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.save(), user)

        login_mock.assert_called_once_with(context['request'], user)
