from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category
from django.db.models.signals import post_save
from .models import BlogRating

@receiver(post_migrate)
def create_categories(sender, **kwargs):
    predefined_categories = ['Tech', 'Lifestyle', 'Health', 'Education']
    for category_name in predefined_categories:
        Category.objects.get_or_create(name=category_name)




@receiver(post_save, sender=BlogRating)
def blog_rating_created(sender, instance, created, **kwargs):
    if created:
        # Do something when a BlogRating is created
        print(f"New rating created: {instance.rating}")