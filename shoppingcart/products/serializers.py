from drf_extra_fields.fields import Base64ImageField
from products.models import Product
from rest_framework.serializers import ModelSerializer


class ProductSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Product
        fields = ['uuid', 'name', 'price', 'image']
