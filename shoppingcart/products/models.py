from django.db import models
from utils.models import Uuidable


class Product(Uuidable):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/product')

    def __str__(self) -> str:
        return self.name
