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


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=130, unique=True)
    content = RichTextField()  # Changed to RichTextField for rich text editing
    image = models.ImageField(upload_to="blog_images", blank=True, null=True)
    dateTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-dateTime']  # Order by dateTime descending

    def __str__(self):
        return f'Blog Post by {self.author.username}: {self.title}'

    def get_absolute_url(self):
        return reverse('blogs')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)   
    dateTime = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.user.username} Comment: {self.content}'
