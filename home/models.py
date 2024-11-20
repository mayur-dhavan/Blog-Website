from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from ckeditor.fields import RichTextField  # Import for rich text field


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True, help_text="Enter your phone number")
    facebook = models.URLField(max_length=300, blank=True, null=True)
    instagram = models.URLField(max_length=300, blank=True, null=True)
    linkedin = models.URLField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Tech', 'Tech'),
        ('Lifestyle', 'Lifestyle'),
        ('Health', 'Health'),
        ('Education', 'Education'),
    ]

    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=130, unique=True)
    content = RichTextField()
    image = models.ImageField(upload_to="blog_images", blank=True, null=True)
    dateTime = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-dateTime']

    def __str__(self):
        return f'Blog Post by {self.author.username}: {self.title}'

    def get_average_rating(self):
        """Calculate and return the average rating of the blog post."""
        ratings = BlogRating.objects.filter(blog=self)
        if ratings.exists():
            return ratings.aggregate(models.Avg('rating'))['rating__avg']
        return None


class BlogRating(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ratings')
    rating = models.IntegerField(default=1)  # Rating on a scale of 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('blog', 'user')  # Ensure each user can rate a blog only once

    def __str__(self):
        return f'{self.user.username} rated {self.blog.title} ({self.rating})'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    dateTime = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.user.username} Comment: {self.content}'
