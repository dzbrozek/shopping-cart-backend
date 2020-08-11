import decimal

from django.test import TestCase
from products.serializers import ProductSerializer
from rest_framework.exceptions import ErrorDetail


class ProductSerializerTest(TestCase):
    def test_create_product(self):
        data = {
            'name': 'Product name',
            'price': '2.25',
            'image': 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
        }
        serializer = ProductSerializer(data=data)

        self.assertTrue(serializer.is_valid(raise_exception=True))
        product = serializer.save()

        self.assertEqual(product.name, data['name'])
        self.assertEqual(product.price, decimal.Decimal(data['price']))
        self.assertTrue(product.image)

    def test_missing_data(self):
        data = {}
        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertDictEqual(
            serializer.errors,
            {
                'image': [ErrorDetail(string='No file was submitted.', code='required')],
                'name': [ErrorDetail(string='This field is required.', code='required')],
                'price': [ErrorDetail(string='This field is required.', code='required')],
            },
        )
