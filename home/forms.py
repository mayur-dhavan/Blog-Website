from django import forms
from .models import Profile, BlogPost, Category, Rating

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
        fields = ('title', 'slug', 'content', 'image', 'category')  # Include 'category' in fields
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title of the Blog'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Copy the title with no space and a hyphen in between'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Content of the Blog'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']  # Only the score field is needed for the rating

    score = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], widget=forms.RadioSelect())
