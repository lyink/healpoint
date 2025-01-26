from django.shortcuts import render
from . import models

from django.shortcuts import render,redirect
from .forms import DataForm
from django.http import HttpResponseRedirect
from django.contrib import messages
#return home.html

def home(request):
    anouncement=models.Doctors.objects.all().order_by('-id')[:4]
    programs=models.Programs.objects.all().order_by('-program_name')[:10]
    best=models.Herroes.objects.all().order_by('-id')[:1]
    return render(request,'home.html',{'announcements':anouncement,'programs':programs,'best':best})

def herroes(request):
    best=models.Herroes.objects.all().order_by('-id')
    return render(request,'herroes.html',{'best':best})

def about(request):
    return render(request,'about.html')

from django.shortcuts import render
from .models import Doctors  # Import the Doctors model

def doctors(request):
    # Fetch all doctors ordered by their ID in descending order
    doctors_list = Doctors.objects.all().order_by('-id')
    
    # Pass the doctors list to the template
    return render(request, 'doctors.html', {'doctors': doctors_list})


def courses(request):
    programs=models.Programs.objects.all().order_by('-program_name')
    return render(request,'courses.html',{'programs':programs})




def application(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"successfully")
            #return HttpResponseRedirect('/')
            return redirect('application')
        else:
            messages.error(request,"Failed")
    else:
         form = DataForm()
         context = {
        'form': form,}
    return render(request, 'application.html', context)


from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post, Category, Tag

def post_list(request):
    posts_list = Post.objects.all().order_by('-publication_date')
    latest_news = Post.objects.all().order_by('-publication_date')[:10]  # Limit to 10 latest posts

    # Filter by category or tag
    category_filter = request.GET.get('category')
    tag_filter = request.GET.get('tag')

    if category_filter:
        posts_list = posts_list.filter(categories__id=category_filter)
        latest_news = latest_news.filter(categories__id=category_filter)

    if tag_filter:
        posts_list = posts_list.filter(tags__id=tag_filter)
        latest_news = latest_news.filter(tags__id=tag_filter)

    # Pagination: 10 posts per page
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')  # Get the current page number from the URL
    posts = paginator.get_page(page_number)  # Get the posts for the current page

    # Get all categories and tags for the filter dropdowns
    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'posts': posts,
        'latest_news': latest_news,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    related_posts = Post.objects.filter(categories__in=post.categories.all()).exclude(id=post.id).distinct()[:5]  # Limit to 5 related posts
    return render(request, 'post_detail.html', {'post': post, 'related_posts': related_posts})

def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(categories=category).order_by('-publication_date')
    return render(request, 'category_posts.html', {'category': category, 'posts': posts})

def tag_posts(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    posts = Post.objects.filter(tags=tag).order_by('-publication_date')
    return render(request, 'tag_posts.html', {'tag': tag, 'posts': posts})


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm  # Optional: Create a form for better validation

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)  # Optional: Use a Django form
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send an email (optional)
            send_mail(
                subject=f"Contact Form Submission from {name}",
                message=message,
                from_email=email,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            # Display a success message
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact_us')
    else:
        form = ContactForm()  # Optional: Initialize an empty form

    return render(request, 'contact_us.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import Doctors

def doctor_detail(request, doctor_id):
    # Fetch the current doctor
    doctor = get_object_or_404(Doctors, id=doctor_id)
    
    # Fetch all other doctors, excluding the current one
    other_doctors = Doctors.objects.exclude(id=doctor_id)
    
    # Pass both the current doctor and other doctors to the template
    return render(request, 'doctor_detail.html', {
        'doctor': doctor,
        'other_doctors': other_doctors,
    })