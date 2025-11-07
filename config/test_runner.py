"""
Custom test runner that excludes .github directory from test discovery
"""

from django.test.runner import DiscoverRunner


class CustomTestRunner(DiscoverRunner):
    """
    Custom test runner that excludes .github and other non-app directories
    from test discovery to prevent import errors.
    """

    def build_suite(self, test_labels=None, **kwargs):
        """
        Build test suite, excluding .github directory.
        If no test labels provided, only test the apps directory.
        """
        # If no specific test labels provided, default to testing only apps
        if not test_labels:
            test_labels = ["apps"]

        return super().build_suite(test_labels=test_labels, **kwargs)
