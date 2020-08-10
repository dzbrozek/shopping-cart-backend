import factory.fuzzy


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'Product {n}')
    price = factory.fuzzy.FuzzyDecimal(low=1, high=100)
    image = factory.django.ImageField(width=1, height=1)

    class Meta:
        model = 'products.Product'
