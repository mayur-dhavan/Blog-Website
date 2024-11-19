from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category

@receiver(post_migrate)
def create_categories(sender, **kwargs):
    predefined_categories = ['Tech', 'Lifestyle', 'Health', 'Education']
    for category_name in predefined_categories:
        Category.objects.get_or_create(name=category_name)
