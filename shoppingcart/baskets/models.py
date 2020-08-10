from django.db import models
from utils.models import Uuidable


class BasketProductRelation(Uuidable):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    basket = models.ForeignKey('baskets.Basket', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self) -> str:
        return f'Basket Product Relation: {self.uuid}'


class Basket(Uuidable):
    products = models.ManyToManyField('products.Product', through=BasketProductRelation, blank=True)
    updated = models.BooleanField(default=False, help_text='Indicates that basket has been updated since last check')

    def __str__(self) -> str:
        return f'Basket: {self.uuid}'
