from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = 'home'

    # Add the `ready` method to import signals
    def ready(self):
        import home.signals  # Import your signals
