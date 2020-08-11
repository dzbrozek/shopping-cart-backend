from django.conf import settings
from django.test.runner import DiscoverRunner


class CustomDiscoverRunner(DiscoverRunner):
    """
    DiscoverRunner that can overwrite settings for the whole process of running tests.

    # example config
    TEST_RUNNER = '<project_path>.runners.CustomDiscoverRunner'
    settings.TEST_SETTINGS = {
        'MEDIA_ROOT': '/test/media/'
    }

    """

    @property
    def new_settings(self):
        return getattr(settings, 'TEST_SETTINGS', {})

    def setup_test_environment(self, **kwargs):
        """
        Save original settings state and override settings
        """
        super().setup_test_environment(**kwargs)
        self.old_settings = {}

        for key, value in self.new_settings.items():
            self.old_settings[key] = getattr(settings, key)
            setattr(settings, key, value)

    def teardown_test_environment(self):
        """
        Restore original settings state.
        """
        super().teardown_test_environment()
        for key, value in self.new_settings.items():
            setattr(settings, key, self.old_settings[key])

        del self.old_settings
