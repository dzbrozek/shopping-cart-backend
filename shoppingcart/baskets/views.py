from typing import Optional

from baskets.models import Basket, BasketProductRelation
from baskets.serializers import BasketProductSerializer, BasketShareSerializer
from django.conf import settings
from django.db import transaction
from products.models import Product
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response


class BasketMixin(GenericAPIView):
    def get_basket(self) -> Optional[Basket]:
        basket_id = self.request.session.get(settings.BASKET_SESSION_ID, None)

        if not basket_id:
            return None

        return Basket.objects.filter(uuid=basket_id).first()

    def get_basket_or_error(self) -> Basket:
        basket = self.get_basket()

        if not basket:
            raise serializers.ValidationError('Missing basket. Please enable cookies.')

        return basket


class BasketAPIView(BasketMixin, GenericAPIView):
    serializer_class = BasketProductSerializer

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        basket = self.get_basket()
        if not basket:
            basket = Basket.objects.create()
            request.session[settings.BASKET_SESSION_ID] = str(basket.uuid)

        basket_products = BasketProductRelation.objects.filter(basket=basket).select_related('product')
        serializer = self.get_serializer(basket_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def delete(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        basket = self.get_basket_or_error()

        BasketProductRelation.objects.filter(basket=basket).delete()
        basket.mark_updated()

        return Response(status=status.HTTP_204_NO_CONTENT)


class BasketShareAPIView(BasketMixin, GenericAPIView):
    serializer_class = BasketShareSerializer

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        basket = self.get_basket_or_error()

        serializer = self.get_serializer(data=request.data, basket=basket)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class BasketProductsAPIView(BasketMixin, GenericAPIView):
    serializer_class = BasketProductSerializer

    @transaction.atomic
    def put(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        basket = self.get_basket_or_error()
        product = get_object_or_404(Product, uuid=kwargs.get('product_id'))
        basket_product, _ = BasketProductRelation.objects.get_or_create(basket=basket, product=product)
        serializer = self.get_serializer(data=request.data, instance=basket_product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        basket.mark_updated()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def delete(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        basket = self.get_basket_or_error()
        product = get_object_or_404(Product, uuid=kwargs.get('product_id'))

        BasketProductRelation.objects.filter(basket=basket, product=product).delete()
        basket.mark_updated()

        return Response(status=status.HTTP_204_NO_CONTENT)
