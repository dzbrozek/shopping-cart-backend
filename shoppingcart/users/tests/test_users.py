from django.test import TestCase
from users.factories import UserFactory


class UsersTest(TestCase):
    def test_user(self):
        user = UserFactory()

        self.assertTrue(user)
