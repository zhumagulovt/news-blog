from factory.django import DjangoModelFactory

from faker import Faker

faker = Faker()


class UserFactory(DjangoModelFactory):

    class Meta:
        model = 'users.CustomUser'

    username = faker.user_name()
    first_name = faker.first_name()
    last_name = faker.last_name()
    password = faker.password()
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)
