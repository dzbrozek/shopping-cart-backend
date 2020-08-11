import uuid

from baskets.factories import BasketFactory, BasketProductRelationFactory
from baskets.models import Basket, BasketProductRelation
from baskets.serializers import BasketProductSerializer
from baskets.views import BASKET_SESSION_ID
from django.core import mail
from django.urls import reverse
from products.factories import ProductFactory
from rest_framework.test import APITestCase
from utils.tests import MediaHttpRequest


class BasketTestMixin:
    def set_up_basket_session(self, basket_id):
        session = self.client.session
        session[BASKET_SESSION_ID] = basket_id
        session.save()


class BasketAPIViewGetTest(BasketTestMixin, APITestCase):
    maxDiff = None

    def setUp(self):
        self.context = dict(request=MediaHttpRequest())

    def test_get_existing_basket(self):
        basket = BasketFactory()
        BasketProductRelationFactory.create_batch(2, basket=basket)

        self.assertEqual(Basket.objects.count(), 1)

        self.set_up_basket_session(str(basket.uuid))

        response = self.client.get(reverse('baskets:basket'))
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            response.json(),
            BasketProductSerializer(
                BasketProductRelation.objects.filter(basket=basket), many=True, context=self.context
            ).data,
        )

        self.assertEqual(Basket.objects.count(), 1)

    def test_create_new_basket(self):
        self.assertEqual(Basket.objects.count(), 0)

        response = self.client.get(reverse('baskets:basket'))
        self.assertEqual(response.status_code, 200)
        basket = Basket.objects.get()
        self.assertListEqual(
            response.json(),
            BasketProductSerializer(
                BasketProductRelation.objects.filter(basket=basket), many=True, context=self.context
            ).data,
        )

        self.assertEqual(Basket.objects.count(), 1)


class BasketAPIViewDeleteTest(BasketTestMixin, APITestCase):
    def test_delete_product_from_basket(self):
        basket = BasketFactory(updated=False)
        BasketProductRelationFactory.create_batch(2, basket=basket)

        self.assertEqual(basket.products.count(), 2)

        self.set_up_basket_session(str(basket.uuid))

        response = self.client.delete(reverse('baskets:basket'))
        self.assertEqual(response.status_code, 204)

        basket.refresh_from_db()
        self.assertTrue(basket.updated)
        self.assertEqual(basket.products.count(), 0)


class BasketShareAPIViewTest(BasketTestMixin, APITestCase):
    def test_share_basket(self):
        basket = BasketFactory()
        BasketProductRelationFactory.create_batch(2, basket=basket)
        self.set_up_basket_session(str(basket.uuid))
        data = {'email': 'share@email.com'}

        response = self.client.post(reverse('baskets:basket-share'), data=data)
        self.assertEqual(response.status_code, 204)

        self.assertEqual(len(mail.outbox), 1)


class BasketProductsAPIViewPutTest(BasketTestMixin, APITestCase):
    maxDiff = None

    def setUp(self):
        self.basket = BasketFactory(updated=False)
        self.product = ProductFactory()
        self.context = dict(request=MediaHttpRequest())

        self.set_up_basket_session(str(self.basket.uuid))

    def test_add_new_product_to_basket(self):
        data = {'quantity': 5}

        response = self.client.put(
            reverse('baskets:basket-products', kwargs=dict(product_id=self.product.uuid)), data=data
        )
        self.assertEqual(response.status_code, 200)
        basket_product = BasketProductRelation.objects.get(product=self.product, basket=self.basket)
        self.assertEqual(basket_product.quantity, 5)
        self.assertDictEqual(response.json(), BasketProductSerializer(basket_product, context=self.context).data)
        self.basket.refresh_from_db()
        self.assertTrue(self.basket.updated)

    def test_update_product_quantity(self):
        basket_product = BasketProductRelationFactory(product=self.product, basket=self.basket, quantity=3)
        data = {'quantity': 2}

        response = self.client.put(
            reverse('baskets:basket-products', kwargs=dict(product_id=self.product.uuid)), data=data
        )
        self.assertEqual(response.status_code, 200)
        basket_product.refresh_from_db()
        self.assertEqual(basket_product.quantity, 2)
        self.assertDictEqual(response.json(), BasketProductSerializer(basket_product, context=self.context).data)
        self.basket.refresh_from_db()
        self.assertTrue(self.basket.updated)

    def test_add_unknown_product(self):
        data = {'quantity': 2}

        response = self.client.put(
            reverse('baskets:basket-products', kwargs=dict(product_id=str(uuid.uuid4()))), data=data
        )
        self.assertEqual(response.status_code, 404)


class BasketProductsAPIViewDeleteTest(BasketTestMixin, APITestCase):
    def setUp(self):
        self.basket = BasketFactory(updated=False)
        self.product = ProductFactory()
        self.basket_product = BasketProductRelationFactory(basket=self.basket, product=self.product, quantity=3)

        self.set_up_basket_session(str(self.basket.uuid))

    def test_delete_existing_product_from_basket(self):
        response = self.client.delete(
            reverse('baskets:basket-products', kwargs=dict(product_id=str(self.product.uuid))),
        )
        self.assertEqual(response.status_code, 204)

        with self.assertRaises(BasketProductRelation.DoesNotExist):
            self.basket_product.refresh_from_db()

        self.basket.refresh_from_db()
        self.assertTrue(self.basket.updated)

    def test_delete_unknown_product_from_basket(self):
        response = self.client.delete(reverse('baskets:basket-products', kwargs=dict(product_id=str(uuid.uuid4()))),)
        self.assertEqual(response.status_code, 404)

        self.basket_product.refresh_from_db()
