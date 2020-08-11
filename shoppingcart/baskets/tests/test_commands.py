from baskets.factories import BasketFactory
from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from users.factories import UserFactory


class CartChangesTest(TestCase):
    def test_no_changes(self):
        BasketFactory(updated=False)

        call_command('cart_changes')

        self.assertEqual(len(mail.outbox), 0)

    def test_no_admin(self):
        BasketFactory(updated=True)

        call_command('cart_changes')

        self.assertEqual(len(mail.outbox), 0)

    def test_send_email(self):
        BasketFactory(updated=False)
        basket = BasketFactory(updated=True)
        UserFactory(is_admin=False, is_active=False)
        UserFactory(is_admin=True, is_active=False)
        admin = UserFactory(is_admin=True, is_active=True)

        call_command('cart_changes')

        self.assertEqual(len(mail.outbox), 1)
        changes_mail = mail.outbox[0]
        self.assertEqual(changes_mail.subject, 'Changed baskets')
        self.assertIn(str(basket.uuid), changes_mail.body)
        self.assertEqual(changes_mail.to, [admin.email])

        basket.refresh_from_db()
        self.assertFalse(basket.updated)
