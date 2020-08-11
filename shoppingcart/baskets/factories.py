import factory.fuzzy


class BasketProductRelationFactory(factory.django.DjangoModelFactory):
    product = factory.SubFactory('products.factories.ProductFactory')
    basket = factory.SubFactory('baskets.factories.BasketFactory')
    quantity = factory.fuzzy.FuzzyInteger(low=1, high=100)

    class Meta:
        model = 'baskets.BasketProductRelation'


class BasketFactory(factory.django.DjangoModelFactory):
    updated = factory.Faker('pybool')

    class Meta:
        model = 'baskets.Basket'
