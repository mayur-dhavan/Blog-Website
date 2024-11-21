from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_no', 'bio', 'facebook', 'instagram', 'linkedin', 'image', )
     
        
class BlogPostForm(forms.ModelForm):
    # Add a category field with a dropdown
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),  # Fetch categories from the database
        required=True,  # Make category selection mandatory
        empty_label="Select a Category",  # Placeholder text
        widget=forms.Select(attrs={'class': 'form-control'})  # Add Bootstrap styling
    )

    class Meta:
        model = BlogPost
        fields = ('title', 'category', 'slug', 'content', 'image')  # Include 'category' in fields
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title of the Blog'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Copy the title with no space and a hyphen in between'}),
            'content': CKEditorWidget(attrs={'class': 'form-control', 'placeholder': 'Content of the Blog','id':'id_content'}),  # Use CKEditor for rich text
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class BlogRatingForm(forms.ModelForm):
    class Meta:
        model = BlogRating
        fields = ['rating']  # We only need the rating field
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1, 'max': 5, 'step': 1,
                'class': 'form-control',
                'placeholder': 'Rate from 1 to 5'
            })
        }
        labels = {
            'rating': 'Rate this blog (1-5):',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Only the content field
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leave a comment here', 'style': 'height: 100px'})
        }