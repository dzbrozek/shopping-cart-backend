from django.urls import reverse
from products.factories import ProductFactory
from products.models import Product
from products.serializers import ProductSerializer
from rest_framework.test import APITestCase
from users.factories import UserFactory
from utils.tests import MediaHttpRequest


class ProductViewSetListTest(APITestCase):
    def test_list_product(self):
        products = ProductFactory.create_batch(2)
        request = MediaHttpRequest()

        response = self.client.get(reverse('products:product-list'))
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            response.json(), ProductSerializer(products, many=True, context=dict(request=request)).data
        )


class ProductViewSetCreateTest(APITestCase):
    def setUp(self):
        self.data = {
            'name': 'Product name',
            'price': '2.25',
            'image': 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
        }

    def test_admin_can_create_product(self):
        user = UserFactory(is_admin=True, is_active=True)
        self.client.force_login(user)

        self.assertFalse(Product.objects.exists())

        response = self.client.post(reverse('products:product-list'), data=self.data)
        self.assertEqual(response.status_code, 201)
        product = Product.objects.get()
        self.assertDictEqual(response.json(), ProductSerializer(product, context=dict(request=MediaHttpRequest())).data)

    def test_unauthorized_user_cannot_create_product(self):
        user = UserFactory(is_admin=False, is_active=True)
        self.client.force_login(user)

        response = self.client.post(reverse('products:product-list'), data=self.data)
        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})

    def test_unauthenticated_user_cannot_create_product(self):
        response = self.client.post(reverse('products:product-list'), data=self.data)
        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})


class ProductViewSetDestroyTest(APITestCase):
    def setUp(self):
        self.product = ProductFactory()

    def test_admin_can_delete_product(self):
        user = UserFactory(is_admin=True, is_active=True)
        self.client.force_login(user)

        response = self.client.delete(reverse('products:product-detail', kwargs=dict(pk=self.product.pk)))
        self.assertEqual(response.status_code, 204)

        with self.assertRaises(Product.DoesNotExist):
            self.product.refresh_from_db()

    def test_unauthorized_user_cannot_delete_product(self):
        user = UserFactory(is_admin=False, is_active=True)
        self.client.force_login(user)

        response = self.client.delete(reverse('products:product-detail', kwargs=dict(pk=self.product.pk)))
        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})

    def test_unauthenticated_user_cannot_delete_product(self):
        response = self.client.delete(reverse('products:product-detail', kwargs=dict(pk=self.product.pk)))
        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})
