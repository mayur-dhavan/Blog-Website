from django.shortcuts import render, redirect,get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from .models import *

from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, BlogPostForm
from django.views.generic import UpdateView
from django.contrib import messages
from .forms import RatingForm


def blogs(request):
    category_filter = request.GET.get('category', None)  # Get the category filter from query parameters
    if category_filter:
        posts = BlogPost.objects.filter(category__name=category_filter).order_by('-dateTime')
    else:
        posts = BlogPost.objects.all().order_by('-dateTime')
    categories = Category.objects.all()  # Fetch all categories for the sidebar or filter options
    return render(request, "blog.html", {'posts': posts, 'categories': categories})



def blogs_comments(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(blog=post)
    if request.method=="POST":
        user = request.user
        content = request.POST.get('content','')
        blog_id =request.POST.get('blog_id','')
        comment = Comment(user = user, content = content, blog=post)
        comment.save()
    return render(request, "blog_comments.html", {'post':post, 'comments':comments})

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
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.category = form.cleaned_data['category']  # Save the selected category
            blogpost.save()
            obj = form.instance
            alert = True
            return render(request, "add_blogs.html", {'obj': obj, 'alert': alert})
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




@login_required
def rate_blog(request, slug):
    blog_post = get_object_or_404(BlogPost, slug=slug)
    user_rating = Rating.objects.filter(user=request.user, blog_post=blog_post).first()

    if request.method == "POST":
        # If user has already rated, we can either update or return an error
        if user_rating:
            # Update existing rating
            user_rating.score = request.POST.get('score')
            user_rating.save()
        else:
            # Create new rating
            form = RatingForm(request.POST)
            if form.is_valid():
                form.instance.user = request.user
                form.instance.blog_post = blog_post
                form.save()

        return redirect('blog_detail', slug=slug)  # Redirect to the blog detail page

    return render(request, 'rate_blog.html', {'blog_post': blog_post, 'user_rating': user_rating})