from baskets.factories import BasketFactory, BasketProductRelationFactory
from baskets.serializers import BasketProductSerializer, BasketShareSerializer
from django.core import mail
from django.test import TestCase
from rest_framework.exceptions import ErrorDetail


class BasketProductRelationTest(TestCase):
    def setUp(self):
        self.basket_product = BasketProductRelationFactory(quantity=3)

    def test_missing_data(self):
        data = {}
        serializer = BasketProductSerializer(self.basket_product, data=data)
        self.assertFalse(serializer.is_valid())
        self.assertDictEqual(
            serializer.errors, {'quantity': [ErrorDetail(string='This field is required.', code='required')]}
        )

    def test_invalid_quantity(self):
        for message, quantity in [['reject zero', 0], ['reject negative value', -5]]:
            with self.subTest(message):
                data = {'quantity': quantity}
                serializer = BasketProductSerializer(self.basket_product, data=data)
                self.assertFalse(serializer.is_valid())
                self.assertDictEqual(
                    serializer.errors,
                    {
                        'quantity': [
                            ErrorDetail(string='Ensure this value is greater than or equal to 1.', code='min_value')
                        ]
                    },
                )

    def test_update_quantity(self):
        data = {'quantity': 5}

        self.assertNotEqual(self.basket_product.quantity, 5)

        serializer = BasketProductSerializer(self.basket_product, data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()

        self.basket_product.refresh_from_db()
        self.assertEqual(self.basket_product.quantity, 5)


class BasketShareSerializerTest(TestCase):
    def setUp(self):
        self.basket = BasketFactory()

    def test_missing_data(self):
        data = {}
        serializer = BasketShareSerializer(basket=self.basket, data=data)
        self.assertFalse(serializer.is_valid())
        self.assertDictEqual(
            serializer.errors, {'email': [ErrorDetail(string='This field is required.', code='required')]}
        )

    def test_invalid_data(self):
        data = {'email': 'trust me I\'m email'}
        serializer = BasketShareSerializer(basket=self.basket, data=data)
        self.assertFalse(serializer.is_valid())
        self.assertDictEqual(
            serializer.errors, {'email': [ErrorDetail(string='Enter a valid email address.', code='invalid')]}
        )

    def test_empty_basket(self):
        data = {'email': 'email@test.com'}
        serializer = BasketShareSerializer(basket=self.basket, data=data)
        self.assertFalse(serializer.is_valid())
        self.assertDictEqual(
            serializer.errors,
            {'non_field_errors': [ErrorDetail(string='Empty basket cannot be shared', code='invalid')]},
        )

    def test_send_email(self):
        data = {'email': 'email@test.com'}
        product = BasketProductRelationFactory(basket=self.basket).product

        serializer = BasketShareSerializer(basket=self.basket, data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()

        self.assertEqual(len(mail.outbox), 1)
        share_mail = mail.outbox[0]
        self.assertEqual(share_mail.subject, 'Check out these products')
        self.assertIn(product.name, share_mail.body)
        self.assertIn(str(product.price), share_mail.body)
        self.assertEqual(share_mail.to, [data['email']])
