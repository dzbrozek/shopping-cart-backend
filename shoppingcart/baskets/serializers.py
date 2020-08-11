from typing import TypedDict

from baskets.models import BasketProductRelation
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from products.serializers import ProductSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer


class BasketProductSerializer(ModelSerializer):
    product = ProductSerializer(read_only=True)
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = BasketProductRelation
        fields = ['uuid', 'product', 'quantity']
        read_only_fields = ['uuid']


class BasketShareSerializerData(TypedDict):
    email: str


class BasketShareSerializer(Serializer):
    email = serializers.EmailField()

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        self.basket = kwargs.pop('basket')

        super().__init__(*args, **kwargs)

    def validate(self, validated_data: BasketShareSerializerData) -> BasketShareSerializerData:
        if not self.basket.products.exists():  # type: ignore
            raise serializers.ValidationError('Empty basket cannot be shared')

        return validated_data

    def save(self, **kwargs: dict) -> None:
        message = render_to_string('baskets/share_basket.txt', {'products': self.basket.products.all()})  # type: ignore
        send_mail(
            'Check out these products',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.validated_data['email']],
            fail_silently=False,
        )
