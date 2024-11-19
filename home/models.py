from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now

from ckeditor.fields import RichTextField  # Import for rich text field


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Link to predefined category

    class Meta:
        ordering = ['-dateTime']

    def __str__(self):
        return f'Blog Post by {self.author.username}: {self.title}'

    def get_average_rating(self):
        ratings = Rating.objects.filter(blog_post=self)
        if ratings.exists():
            total = sum([rating.score for rating in ratings])
            return total / ratings.count()
        return None
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Ratings from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'blog_post')  # Ensure a user can only rate a blog post once

    def __str__(self):
        return f'{self.user.username} rated {self.blog_post.title} with {self.score} stars'
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)   
    dateTime = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.user.username} Comment: {self.content}'
