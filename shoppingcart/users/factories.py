import factory

USER_PASSWORD = 'password'


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda n: f'test-{n}@test.com')
    password = factory.PostGenerationMethodCall('set_password', USER_PASSWORD)
    is_active = factory.Faker('pybool')
    is_admin = factory.Faker('pybool')

    class Meta:
        model = 'users.User'
        django_get_or_create = ('email',)
