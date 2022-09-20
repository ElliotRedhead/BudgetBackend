import factory

from user.models import User


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")
    password = factory.Faker("password")

    class Meta:
        model = User
