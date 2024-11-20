from django.shortcuts import render, redirect,get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from .models import *
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, BlogPostForm
from django.views.generic import UpdateView
from django.contrib import messages
from django.http import JsonResponse
from .forms import BlogRatingForm


def blogs(request):
    category_filter = request.GET.get('category', None)  # Get the category filter from query parameters
    if category_filter:
        posts = BlogPost.objects.filter(category__name=category_filter).order_by('-dateTime')
    else:
        posts = BlogPost.objects.all().order_by('-dateTime')
    
    # Calculate the average rating for each post
    for post in posts:
        ratings = BlogRating.objects.filter(blog=post)  # Get ratings for the current post
        if ratings.exists():
            # Calculate the average rating for this post
            average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
            post.average_rating = average_rating  # Add average_rating to the post object
        else:
            post.average_rating = None  # No ratings yet
    
    categories = Category.objects.all()  # Fetch all categories for the sidebar or filter options

    # Return the updated posts along with categories to the template
    return render(request, "blog.html", {'posts': posts, 'categories': categories})


@login_required(login_url='/login')
def blogs_comments(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    comments = Comment.objects.filter(blog=post)
    
    # Initialize variables for user rating and average rating
    user_rating = None
    average_rating = None

    # Check if the user is authenticated
    if request.user.is_authenticated:
        try:
            # Get the user's rating for the blog (if it exists)
            user_rating = BlogRating.objects.get(blog=post, user=request.user)
        except BlogRating.DoesNotExist:
            user_rating = None

        # Handle form submission for rating
        if request.method == "POST" and 'rating' in request.POST:
            form = BlogRatingForm(request.POST)
            if form.is_valid():
                # Save or update the user's rating for this blog
                rating = form.save(commit=False)
                rating.blog = post
                rating.user = request.user

                if user_rating:
                    # If the user already rated, update their rating
                    user_rating.rating = rating.rating
                    user_rating.save()
                    messages.success(request, "Your rating has been updated!")
                else:
                    # Otherwise, create a new rating
                    rating.save()
                    messages.success(request, "Your rating has been submitted!")

                return redirect('blogs_comments', slug=slug)  # Redirect to prevent duplicate submissions
        else:
            # If the form is not submitted, use the existing rating if the user has one
            form = BlogRatingForm(instance=user_rating)
    else:
        form = None

    # Calculate the average rating for the blog
    ratings = BlogRating.objects.filter(blog=post)
    if ratings.exists():
        average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

    return render(request, "blog_comments.html", {
        'post': post,
        'comments': comments,
        'user_rating': user_rating,
        'average_rating': average_rating,
        'form': form,  # Pass the form to the template
    })


def Delete_Blog_Post(request, slug):
    posts = BlogPost.objects.get(slug=slug)
    if request.method == "POST":
        posts.delete()
        return redirect('/')
    return render(request, 'delete_blog_post.html', {'posts':posts})


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        category_filter = request.POST.get('category', None)
        if category_filter:
            blogs = BlogPost.objects.filter(title__icontains=searched, category__name=category_filter)
        else:
            blogs = BlogPost.objects.filter(title__icontains=searched)
        categories = Category.objects.all()
        return render(request, "search.html", {'searched': searched, 'blogs': blogs, 'categories': categories})
    else:
        categories = Category.objects.all()
        return render(request, "search.html", {'categories': categories})


@login_required(login_url='/login')
def add_blogs(request):
    if request.method == "POST":
        print("POST Data:", request.POST)  # Print the POST data to the console
        print("Files Data:", request.FILES)  # Print the uploaded files
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.category = form.cleaned_data['category']  # Save the selected category
            blogpost.save()
            # Show success message using Django's messages framework
            messages.success(request, 'Your blog has been added successfully!')
            return redirect('blogs')  # Redirect to the homepage or another view
        else:
            # Log form errors and show error message
            print(form.errors)
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = BlogPostForm()

    return render(request, "add_blogs.html", {'form': form})




class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'edit_blog_post.html'
    fields = ['title', 'slug', 'content', 'image', 'category']  # Add the category field



def user_profile(request, myid):
    post = BlogPost.objects.filter(id=myid)
    return render(request, "user_profile.html", {'post':post})

def Profile(request):
    return render(request, "profile.html")

def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method=="POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "edit_profile.html", {'alert':alert})
    else:
        form=ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {'form':form})


def Register(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')
        
        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'login.html')   
    return render(request, "register.html")

def Login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
        return render(request, 'blog.html')   
    return render(request, "login.html")

def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')

from django.shortcuts import render

def privacy_policy(request):
    return render(request, 'privacy-policy.html')

def terms_of_service(request):
    return render(request, 'terms-of-service.html')

def contact(request):
    return render(request, 'contact.html')

