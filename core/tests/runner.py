from django.test.runner import DiscoverRunner as BaseRunner
from decouple import config
from accounts.models import *
from blog.models import *


# for unit test
class TestRunnerMixin(object):
    """a custom test mixin for all tests"""

    def setup_databases(self, *args, **kwargs):
        temp_return = super(TestRunnerMixin, self).setup_databases(*args, **kwargs)
        # * custom commands
        User.objects.create(
            email=config("EMAIL", cast=str),
            password=config("DJANGO_SUPERUSER_PASSWORD", cast=str),
            is_superuser=True,
            is_staff=True,
            is_active=True,
            is_verified=True,
        )
        Category.objects.create(name="test")
        return temp_return

    def teardown_databases(self, *args, **kwargs):
        return super(TestRunnerMixin, self).teardown_databases(*args, **kwargs)


class TestRunner(TestRunnerMixin, BaseRunner):
    """a custom test runner"""

    pass
