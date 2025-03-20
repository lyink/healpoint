import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib import messages
from django.views import View
from django.utils import timezone
from django.core.cache import cache
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Sum
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta

from . import models
from .forms import RentalLoginForm

# Import the custom user model using settings.AUTH_USER_MODEL
from django.contrib.auth import get_user_model
User = get_user_model()

# Home view
from django.shortcuts import render
from django.db.models import Count, Q  # Import Q directly
from .models import RentalProperty, PropertyType

from django.shortcuts import render
from django.db.models import Count, Q
from django.shortcuts import render
from django.db.models import Count, Q, Min, Max
from .models import RentalProperty, PropertyType, TeamMember

def home(request):
    # Get 3 featured properties (recently added with available status)
    featured_properties = RentalProperty.objects.filter(
        status='available'
    ).prefetch_related(
        'images'  # Prefetch the related images
    ).order_by('-id')[:3]
    
    # Get all property types with count of available properties for each
    property_types = PropertyType.objects.annotate(
        available_count=Count('rentalproperty', filter=Q(rentalproperty__status='available'))
    )
    
    # Get team members for display on homepage
    team_members = TeamMember.objects.all().order_by('name')
    
    # Get unique cities from the database
    cities = RentalProperty.objects.filter(status='available').values_list('city', flat=True).distinct().order_by('city')
    
    # Calculate price ranges based on actual rental prices
    min_price = RentalProperty.objects.filter(status='available').aggregate(min_price=Min('monthly_rent'))['min_price'] or 0
    max_price = RentalProperty.objects.filter(status='available').aggregate(max_price=Max('monthly_rent'))['max_price'] or 0
    
    # Create dynamic price ranges
    price_ranges = []
    if max_price > 0:
        # Round min and max prices to nearest 500
        min_price_rounded = (min_price // 500) * 500
        max_price_rounded = ((max_price // 500) + 1) * 500
        
        # Create price range steps
        step = 1000
        current = min_price_rounded
        
        while current < max_price_rounded:
            next_step = current + step
            if next_step >= max_price_rounded:
                price_ranges.append({
                    'min': current,
                    'max': '',
                    'display': f'${current:,}+'
                })
            else:
                price_ranges.append({
                    'min': current,
                    'max': next_step,
                    'display': f'${current:,} - ${next_step:,}'
                })
            current = next_step
    
    context = {
        'featured_properties': featured_properties,
        'property_types': property_types,
        'team_members': team_members,
        'cities': cities,
        'price_ranges': price_ranges,
    }
    
    return render(request, 'home.html', context)
def about(request):
    return render(request, 'about.html')

# Doctors view


class LoginView(View):
    """
    Enhanced user login functionality with email authentication
    """
    template_name = 'accounts/login.html'
    form_class = RentalLoginForm

    def get(self, request, *args, **kwargs):
        """
        Display the login form with enhanced security checks
        """
        # If user is already authenticated, redirect to dashboard
        if request.user.is_authenticated:
            return redirect('dashboard')
        
        # Clear any previous login attempt cache
        self.clear_login_attempts_cache(request)
        
        form = self.form_class()
        return render(request, self.template_name, {
            'form': form,
            'title': 'Login to RentalHub'
        })

    def post(self, request, *args, **kwargs):
        """
        Process the login form submission with robust security measures
        """
        # Check for excessive login attempts
        if self.is_login_attempt_blocked(request):
            messages.error(request, 'Too many login attempts. Please try again later.')
            return render(request, self.template_name, {
                'form': self.form_class(),
                'title': 'Login Blocked'
            })
        
        form = self.form_class(data=request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            # Since USERNAME_FIELD is 'email', we can directly authenticate with email
            # Django will internally treat the first parameter as an email
            auth_user = authenticate(request, username=email, password=password)
            
            if auth_user is not None:
                # Clear any existing sessions for this user
                self.clear_existing_sessions(auth_user)
                
                # Log in the user
                auth_login(request, auth_user)
                
                # Set session expiry based on remember me
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser is closed
                else:
                    # Set a longer session if remember me is checked
                    request.session.set_expiry(1209600)  # 2 weeks
                
                # Clear login attempt tracking
                self.clear_login_attempts_cache(request)
                
                # Set success message
                messages.success(request, f'Welcome back, {auth_user.first_name or auth_user.username}!')
                
                # Redirect to dashboard after successful login
                return redirect('dashboard')
            else:
                # Failed login attempt
                self.track_login_attempt(request, email)
                messages.error(request, 'Invalid email or password')
        
        return render(request, self.template_name, {
            'form': form,
            'title': 'Login to RentalHub'
        })

    def track_login_attempt(self, request, email):
        """
        Track and limit login attempts
        """
        # Use cache to track login attempts
        cache_key = f'login_attempts_{request.META.get("REMOTE_ADDR")}'
        attempts = cache.get(cache_key, 0) + 1
        
        # Block after 5 consecutive failed attempts
        if attempts >= 5:
            # Set a 15-minute block
            cache.set(cache_key, attempts, 900)  # 15 * 60 seconds
        else:
            # Increment attempts
            cache.set(cache_key, attempts, 900)  # 15 minutes window
    
    def is_login_attempt_blocked(self, request):
        """
        Check if login attempts are blocked
        """
        cache_key = f'login_attempts_{request.META.get("REMOTE_ADDR")}'
        attempts = cache.get(cache_key, 0)
        return attempts >= 5
    
    def clear_login_attempts_cache(self, request):
        """
        Clear login attempts tracking
        """
        cache_key = f'login_attempts_{request.META.get("REMOTE_ADDR")}'
        cache.delete(cache_key)
    
    def clear_existing_sessions(self, user):
        """
        Terminate existing sessions for the user
        """
        # Remove all existing sessions for this user
        for session in Session.objects.filter(expire_date__gte=timezone.now()):
            session_data = session.get_decoded()
            if '_auth_user_id' in session_data and int(session_data.get('_auth_user_id', 0)) == user.id:
                session.delete()
@login_required
@require_http_methods(["POST"])
def logout_view(request):
    """
    Secure logout view
    """
    # Clear all user sessions
    Session.objects.filter(
        expire_date__gte=timezone.now(),
        session_data__contains=str(request.user.id)
    ).delete()
    
    # Log out the user
    logout(request)
    
    # Clear all messages
    storage = messages.get_messages(request)
    storage.used = True
    
    # Add logout message
    messages.success(request, 'You have been successfully logged out.')
    
    return redirect('login')

# Dashboard views
@login_required
def dashboard_view(request):
    """
    Main dashboard view for authenticated users.
    Displays summary of properties, appointments, favorites and messages.
    """
    # Get user's active listings (if user is landlord)
    active_listings_count = 0
    if hasattr(request.user, 'profile') and getattr(request.user.profile, 'is_landlord', False):
        # This assumes you have a Property model with a foreign key to settings.AUTH_USER_MODEL
        active_listings_count = request.user.properties.filter(is_active=True).count()
    
    # Get upcoming appointments
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    
    # This assumes you have an Appointment model with a foreign key to settings.AUTH_USER_MODEL
    upcoming_appointments = []
    upcoming_appointments_count = 0
    
    try:
        upcoming_appointments = request.user.appointments.filter(
            date__gte=today,
            date__lte=next_week,
            status__in=['confirmed', 'pending']
        ).order_by('date')[:5]
        
        upcoming_appointments_count = upcoming_appointments.count()
    except AttributeError:
        # Handle case where appointments model might not be set up yet
        pass
    
    # Get saved/favorite properties
    saved_properties_count = 0
    recently_viewed_properties = []
    
    try:
        saved_properties_count = request.user.favorites.count()
        recently_viewed_properties = request.user.property_views.order_by('-viewed_at')[:4]
    except AttributeError:
        # Handle case where favorites model might not be set up yet
        pass
    
    # Get unread messages count
    unread_messages_count = 0
    try:
        unread_messages_count = request.user.messages.filter(is_read=False).count()
    except AttributeError:
        pass
    
    # Get recent activity
    recent_activities = []
    try:
        recent_activities = request.user.activities.order_by('-timestamp')[:5]
    except AttributeError:
        pass
    
    # Create context dictionary with all data for the template
    context = {
        'active_page': 'dashboard',
        'active_listings_count': active_listings_count,
        'upcoming_appointments_count': upcoming_appointments_count,
        'saved_properties_count': saved_properties_count,
        'unread_messages_count': unread_messages_count,
        'upcoming_appointments': upcoming_appointments,
        'recently_viewed_properties': recently_viewed_properties,
        'recent_activities': recent_activities,
        'notification_count': unread_messages_count,  # For the topbar notification badge
    }
    
    return render(request, 'dashboard.html', context)

# Properties Views
@login_required
def my_properties_view(request):
    """View for managing user's properties (for landlords)"""
    context = {
        'active_page': 'my_properties',
    }
    return render(request, 'properties/my_properties.html', context)

@login_required
def browse_properties_view(request):
    """View for browsing available properties"""
    context = {
        'active_page': 'browse_properties',
    }
    return render(request, 'properties/browse.html', context)

@login_required
def favorites_view(request):
    """View for user's favorite/saved properties"""
    context = {
        'active_page': 'favorites',
    }
    return render(request, 'properties/favorites.html', context)

# Appointments View
@login_required
def appointments_view(request):
    """View for managing property viewing appointments"""
    context = {
        'active_page': 'appointments',
    }
    return render(request, 'appointments/index.html', context)

# Payments View
@login_required
def payments_view(request):
    """View for managing rental payments"""
    context = {
        'active_page': 'payments',
    }
    return render(request, 'payments/index.html', context)

# Settings View
@login_required
def settings_view(request):
    """View for user account settings"""
    context = {
        'active_page': 'settings',
    }
    return render(request, 'settings/index.html', context)

# Support View
@login_required
def support_view(request):
    """View for help and support"""
    context = {
        'active_page': 'support',
    }
    return render(request, 'support/index.html', context)

def home_redirect(request):
    """Redirect to dashboard if logged in, otherwise to login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')
    


# User management views
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def user_management(request):
    """
    View to manage users with search and filtering capabilities
    """
    # Get query parameters
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    role = request.GET.get('role', '')

    # Base queryset - using User from get_user_model()
    users = User.objects.all().order_by('-date_joined')

    # Filter by search query
    if query:
        users = users.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(email__icontains=query)
        )

    # Filter by account status
    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)

    # Filter by role (assuming you have a custom profile model)
    if role:
        users = users.filter(profile__role=role)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(users, 10)  # 10 users per page

    try:
        users_page = paginator.page(page)
    except PageNotAnInteger:
        users_page = paginator.page(1)
    except EmptyPage:
        users_page = paginator.page(paginator.num_pages)

    context = {
        'users': users_page,
        'query': query,
        'status': status,
        'role': role,
        'total_users': users.count(),
        'active_users': users.filter(is_active=True).count(),
        'inactive_users': users.filter(is_active=False).count(),
        'active_page': 'user_management'
    }

    return render(request, 'accounts/user_management.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import User

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def user_details(request, user_id):
    """
    View to show detailed information about a specific user
    """
    user = get_object_or_404(User, id=user_id)
    
    context = {
        'user_detail': user,
        'active_page': 'user_management'
    }
    
    return render(request, 'accounts/user_details.html', context)

@login_required
def update_profile_pic(request, user_id):
    """
    View to handle profile picture upload/removal
    """
    user = get_object_or_404(User, id=user_id)
    
    # Check if the current user has permission to modify this user
    if not (request.user.is_staff or request.user.is_superuser or request.user.id == user.id):
        messages.error(request, "You don't have permission to modify this user's profile picture.")
        return redirect('user_details', user_id=user_id)
    
    if request.method == 'POST':
        if 'remove_pic' in request.POST:
            # Remove the profile picture
            user.profile_pic_data = None
            user.profile_pic_type = None
            user.save()
            messages.success(request, "Profile picture removed successfully.")
        elif 'profile_pic' in request.FILES:
            # Upload new profile picture
            try:
                user.set_profile_pic(request.FILES['profile_pic'])
                user.save()
                messages.success(request, "Profile picture updated successfully.")
            except ValueError as e:
                messages.error(request, str(e))
        
    return redirect('user_details', user_id=user_id)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def toggle_user_status(request, user_id):
    """
    View to toggle a user's active status
    """
    user = get_object_or_404(User, id=user_id)
    
    # Prevent deactivating yourself
    if request.user == user:
        messages.error(request, "You cannot change your own status.")
        return redirect('user_details', user_id=user_id)
    
    # Toggle the status
    user.is_active = not user.is_active
    user.save()
    
    status = "activated" if user.is_active else "deactivated"
    messages.success(request, f"User {user.username} has been {status}.")
    
    return redirect('user_details', user_id=user_id)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def delete_user(request, user_id):
    """
    View to delete a user
    """
    user = get_object_or_404(User, id=user_id)
    
    # Prevent deleting yourself
    if request.user == user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('user_details', user_id=user_id)
    
    # Prevent deleting superusers
    if user.is_superuser:
        messages.error(request, "Superuser accounts cannot be deleted from this interface.")
        return redirect('user_details', user_id=user_id)
    
    username = user.username
    user.delete()
    
    messages.success(request, f"User {username} has been deleted.")
    return redirect('user_management')




# APP1/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.sessions.models import Session
from django.core.cache import cache
from datetime import datetime, timedelta

from .forms import RentalLoginForm, UserRegistrationForm, ProfileUpdateForm
from .models import User, Profile, Property, Appointment, Message, Activity




from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm

User = get_user_model()

@login_required
def create_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Hash password
            
            # Process profile picture
            profile_pic = form.cleaned_data.get('profile_pic')
            if profile_pic:
                user.set_profile_pic(profile_pic)
            
            user.save()
            messages.success(request, "User created successfully!")
            return redirect("user_management")  # Change this to the correct redirect URL
    else:
        form = UserRegistrationForm()
    
    return render(request, "accounts/register.html", {"form": form})



class RegisterView(View):
    """
    User registration with validation
    """
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm

    def get(self, request, *args, **kwargs):
        # If user is already authenticated, redirect to dashboard
        if request.user.is_authenticated:
            return redirect('dashboard')
        
        form = self.form_class()
        return render(request, self.template_name, {
            'form': form,
            'title': 'Register for RentalHub'
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        
        if form.is_valid():
            # Create user but don't save yet
            user = form.save(commit=False)
            # Additional processing if needed
            user.save()
            
            # Create user profile
            Profile.objects.create(user=user)
            
            # Log activity
            Activity.objects.create(
                user=user,
                description="Account created"
            )
            
            messages.success(request, 'Your account has been created successfully. You can now login.')
            return redirect('login')
        
        return render(request, self.template_name, {
            'form': form,
            'title': 'Register for RentalHub'
        })

@login_required
@require_http_methods(["POST"])
def logout_view(request):
    """
    Secure logout view
    """
    # Clear all user sessions
    Session.objects.filter(
        expire_date__gte=timezone.now(),
        session_data__contains=str(request.user.id)
    ).delete()
    
    # Log out the user
    logout(request)
    
    # Clear all messages
    storage = messages.get_messages(request)
    storage.used = True
    
    # Add logout message
    messages.success(request, 'You have been successfully logged out.')
    
    return redirect('login')

# Dashboard views
@login_required
def dashboard_view(request):
    """
    Main dashboard view for authenticated users.
    Displays summary of properties, appointments, favorites and messages.
    """
    # Get user's active listings (if user is landlord)
    active_listings_count = 0
    if hasattr(request.user, 'profile') and getattr(request.user.profile, 'is_landlord', False):
        # This assumes you have a Property model with a foreign key to settings.AUTH_USER_MODEL
        active_listings_count = Property.objects.filter(owner=request.user, is_active=True).count()
    
    # Get upcoming appointments
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    
    # This assumes you have an Appointment model with a foreign key to settings.AUTH_USER_MODEL
    upcoming_appointments = []
    upcoming_appointments_count = 0
    
    try:
        upcoming_appointments = Appointment.objects.filter(
            user=request.user,
            date__gte=today,
            date__lte=next_week,
            status__in=['confirmed', 'pending']
        ).order_by('date')[:5]
        
        upcoming_appointments_count = upcoming_appointments.count()
    except Exception:
        # Handle case where appointments model might not be set up yet
        pass
    
    # Get saved/favorite properties
    saved_properties_count = 0
    recently_viewed_properties = []
    
    try:
        saved_properties_count = request.user.favorites.count()
        recently_viewed_properties = request.user.property_views.order_by('-viewed_at')[:4]
    except Exception:
        # Handle case where favorites model might not be set up yet
        pass
    
    # Get unread messages count
    unread_messages_count = 0
    try:
        unread_messages_count = Message.objects.filter(recipient=request.user, is_read=False).count()
    except Exception:
        pass
    
    # Get recent activity
    recent_activities = []
    try:
        recent_activities = Activity.objects.filter(user=request.user).order_by('-timestamp')[:5]
    except Exception:
        pass
    
    # Create context dictionary with all data for the template
    context = {
        'active_page': 'dashboard',
        'active_listings_count': active_listings_count,
        'upcoming_appointments_count': upcoming_appointments_count,
        'saved_properties_count': saved_properties_count,
        'unread_messages_count': unread_messages_count,
        'upcoming_appointments': upcoming_appointments,
        'recently_viewed_properties': recently_viewed_properties,
        'recent_activities': recent_activities,
        'notification_count': unread_messages_count,  # For the topbar notification badge
    }
    
    return render(request, 'dashboard.html', context)

# Properties Views
@login_required
def my_properties_view(request):
    """View for managing user's properties (for landlords)"""
    properties = Property.objects.filter(owner=request.user).order_by('-created_at')
    
    context = {
        'active_page': 'my_properties',
        'properties': properties
    }
    return render(request, 'properties/my_properties.html', context)

@login_required
def browse_properties_view(request):
    """View for browsing available properties"""
    properties = Property.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'active_page': 'browse_properties',
        'properties': properties
    }
    return render(request, 'properties/browse.html', context)

@login_required
def favorites_view(request):
    """View for user's favorite/saved properties"""
    favorites = request.user.favorites.all().order_by('-created_at')
    
    context = {
        'active_page': 'favorites',
        'favorites': favorites
    }
    return render(request, 'properties/favorites.html', context)

# Appointments View
@login_required
def appointments_view(request):
    """View for managing property viewing appointments"""
    appointments = Appointment.objects.filter(user=request.user).order_by('-date')
    
    context = {
        'active_page': 'appointments',
        'appointments': appointments
    }
    return render(request, 'appointments/index.html', context)

# Payments View
@login_required
def payments_view(request):
    """View for managing rental payments"""
    context = {
        'active_page': 'payments',
    }
    return render(request, 'payments/index.html', context)

# Settings View
@login_required
def settings_view(request):
    """View for user account settings"""
    initial_data = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    
    if hasattr(request.user, 'profile'):
        initial_data.update({
            'phone_number': request.user.profile.phone_number,
            'address': request.user.profile.address,
            'is_landlord': request.user.profile.is_landlord,
        })
    
    form = ProfileUpdateForm(initial=initial_data)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            # Update user info
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            
            if form.cleaned_data.get('profile_pic'):
                request.user.profile_pic = form.cleaned_data['profile_pic']
            
            request.user.save()
            
            # Update profile info
            profile = request.user.profile
            profile.phone_number = form.cleaned_data['phone_number']
            profile.address = form.cleaned_data['address']
            profile.is_landlord = form.cleaned_data['is_landlord']
            profile.save()
            
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('settings')
    
    context = {
        'active_page': 'settings',
        'form': form
    }
    return render(request, 'settings/index.html', context)

# Support View
@login_required
def support_view(request):
    """View for help and support"""
    context = {
        'active_page': 'support',
    }
    return render(request, 'support/index.html', context)

def home_redirect(request):
    """Redirect to dashboard if logged in, otherwise to login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')

# User management views
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def user_management(request):
    """
    View to manage users with search and filtering capabilities
    """
    # Get query parameters
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    role = request.GET.get('role', '')

    # Base queryset - using User from get_user_model()
    users = User.objects.all().order_by('-date_joined')

    # Filter by search query
    if query:
        users = users.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(email__icontains=query)
        )

    # Filter by account status
    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)

    # Filter by role (from User model)
    if role:
        users = users.filter(role=role)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(users, 10)  # 10 users per page

    try:
        users_page = paginator.page(page)
    except PageNotAnInteger:
        users_page = paginator.page(1)
    except EmptyPage:
        users_page = paginator.page(paginator.num_pages)

    context = {
        'users': users_page,
        'query': query,
        'status': status,
        'role': role,
        'total_users': users.count(),
        'active_users': users.filter(is_active=True).count(),
        'inactive_users': users.filter(is_active=False).count(),
        'active_page': 'user_management'
    }

    return render(request, 'accounts/user_management.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def user_details(request, user_id):
    """
    View to show detailed information about a specific user
    """
    user = get_object_or_404(User, id=user_id)
    
    context = {
        'user_detail': user,
        'active_page': 'user_management'
    }
    
    return render(request, 'accounts/user_details.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def toggle_user_status(request, user_id):
    """
    View to activate or deactivate a user account
    """
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        
        # Toggle user status
        user.is_active = not user.is_active
        user.save()
        
        # Add message
        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f'User {user.username} has been {status} successfully.')
        
        return redirect('user_management')
    
    # If not a POST request, redirect to user management
    return redirect('user_management')

######################################################################################################################################################################
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Location, Regions, Districts, Wards
from .forms import LocationForm

class LocationListView(ListView):
    model = Location
    template_name = 'locations/location_list.html'
    context_object_name = 'locations'
    paginate_by = 10

class LocationDetailView(DetailView):
    model = Location
    template_name = 'locations/location_detail.html'
    context_object_name = 'location'

class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'locations/location_form.html'
    success_url = reverse_lazy('location_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_maps_api_key'] = 'YOUR_GOOGLE_MAPS_API_KEY'  # Replace with your actual API key
        context['is_create'] = True
        return context

class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'locations/location_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_maps_api_key'] = 'YOUR_GOOGLE_MAPS_API_KEY'  # Replace with your actual API key
        context['is_create'] = False
        return context
    
    def get_success_url(self):
        return reverse('location_detail', kwargs={'pk': self.object.pk})

class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Location
    template_name = 'locations/location_confirm_delete.html'
    success_url = reverse_lazy('location_list')

# AJAX views for dependent dropdowns
def load_districts(request):
    region_id = request.GET.get('region')
    districts = Districts.objects.filter(mkoa_id=region_id).order_by('dname')
    return render(request, 'locations/district_dropdown_list_options.html', {'districts': districts})

def load_wards(request):
    district_id = request.GET.get('district')
    wards = Wards.objects.filter(wilaya=district_id).order_by('wname')
    return render(request, 'locations/ward_dropdown_list_options.html', {'wards': wards})

#################################################################################################################################################################
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

from .models import PropertyType, RentalProperty, PropertyImage
from .forms import PropertyTypeForm, RentalPropertyForm, PropertyImageForm

# PropertyType Views
class PropertyTypeListView(ListView):
    model = PropertyType
    template_name = 'property/property_type_list.html'
    context_object_name = 'property_types'
    ordering = ['name']


class PropertyTypeDetailView(DetailView):
    model = PropertyType
    template_name = 'property/property_type_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = RentalProperty.objects.filter(property_type=self.object)
        return context


class PropertyTypeCreateView(LoginRequiredMixin, CreateView):
    model = PropertyType
    form_class = PropertyTypeForm
    template_name = 'property/property_type_form.html'
    success_url = reverse_lazy('property_type_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Property type created successfully.')
        return super().form_valid(form)


class PropertyTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = PropertyType
    form_class = PropertyTypeForm
    template_name = 'property/property_type_form.html'
    success_url = reverse_lazy('property_type_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Property type updated successfully.')
        return super().form_valid(form)


class PropertyTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = PropertyType
    template_name = 'property/property_type_confirm_delete.html'
    success_url = reverse_lazy('property_type_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Property type deleted successfully.')
        return super().delete(request, *args, **kwargs)


from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class RentalPropertyListView(LoginRequiredMixin, ListView):
    model = RentalProperty
    template_name = 'property/rental_property_list.html'
    context_object_name = 'properties'
    ordering = ['-status', 'name']
    paginate_by = 10

    def get_queryset(self):
        """
        Filter the queryset based on search query, status, and property type.
        """
        queryset = super().get_queryset()
        
        # Search filter
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(address__icontains=query) |
                Q(city__icontains=query) |
                Q(state__icontains=query)
            )
        
        # Status filter
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Property type filter
        property_type = self.request.GET.get('property_type')
        if property_type:
            queryset = queryset.filter(property_type__id=property_type)
        
        return queryset

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        
        # Add property types for the dropdown
        context['property_types'] = PropertyType.objects.all()
        
        # Add property statuses for the dropdown
        context['statuses'] = dict(RentalProperty.PROPERTY_STATUS)
        
        return context

class RentalPropertyDetailView(DetailView):
    model = RentalProperty
    template_name = 'property/rental_property_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = PropertyImage.objects.filter(property=self.object).order_by('display_order')
        return context


from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

class RentalPropertyCreateView(LoginRequiredMixin, CreateView):
    model = RentalProperty
    form_class = RentalPropertyForm
    template_name = 'property/rental_property_form.html'
    success_url = reverse_lazy('rental_property_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Create the image formset
        ImageFormSet = inlineformset_factory(
            RentalProperty,  # Parent model
            PropertyImage,   # Child model
            form=PropertyImageForm,
            extra=3,  # Number of empty forms to display
            can_delete=True
        )
        
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = ImageFormSet()
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        
        # Validate both the main form and the image formset
        if form.is_valid() and image_formset.is_valid():
            form.instance.owner = self.request.user
            self.object = form.save()
            
            # Save the image formset with the property instance
            image_formset.instance = self.object
            image_formset.save()
            
            messages.success(self.request, 'Property created successfully.')
            return super().form_valid(form)
        else:
            # If validation fails, re-render the form with errors
            return self.render_to_response(self.get_context_data(form=form))

class RentalPropertyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RentalProperty
    form_class = RentalPropertyForm
    template_name = 'property/rental_property_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Create the image formset with existing images
        ImageFormSet = inlineformset_factory(
            RentalProperty,  # Parent model
            PropertyImage,   # Child model
            form=PropertyImageForm,
            extra=3,  # Number of empty forms to display
            can_delete=True
        )
        
        if self.request.POST:
            context['image_formset'] = ImageFormSet(
                self.request.POST, 
                self.request.FILES, 
                instance=self.object
            )
        else:
            context['image_formset'] = ImageFormSet(instance=self.object)
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        
        # Validate both the main form and the image formset
        if form.is_valid() and image_formset.is_valid():
            self.object = form.save()
            
            # Save the image formset with the property instance
            image_formset.instance = self.object
            image_formset.save()
            
            messages.success(self.request, 'Property updated successfully.')
            return super().form_valid(form)
        else:
            # If validation fails, re-render the form with errors
            return self.render_to_response(self.get_context_data(form=form))

    # Other methods from your original view remain the same
    
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user
    
    def get_success_url(self):
        return reverse_lazy('rental_property_detail', kwargs={'pk': self.object.pk})

class RentalPropertyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RentalProperty
    template_name = 'property/rental_property_confirm_delete.html'
    success_url = reverse_lazy('rental_property_list')
    
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Property deleted successfully.')
        return super().delete(request, *args, **kwargs)


# PropertyImage Views
class PropertyImageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PropertyImage
    form_class = PropertyImageForm
    template_name = 'property/property_image_form.html'
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.property = get_object_or_404(RentalProperty, pk=kwargs.get('property_pk'))
    
    def test_func(self):
        return self.property.owner == self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property'] = self.property
        return context
    
    def form_valid(self, form):
        form.instance.property = self.property
        messages.success(self.request, 'Image uploaded successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('rental_property_detail', kwargs={'pk': self.property.pk})


class PropertyImageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PropertyImage
    form_class = PropertyImageForm
    template_name = 'property/property_image_form.html'
    
    def test_func(self):
        obj = self.get_object()
        return obj.property.owner == self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property'] = self.object.property
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Image updated successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('rental_property_detail', kwargs={'pk': self.object.property.pk})


class PropertyImageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PropertyImage
    template_name = 'property/property_image_confirm_delete.html'
    
    def test_func(self):
        obj = self.get_object()
        return obj.property.owner == self.request.user
    
    def get_success_url(self):
        return reverse_lazy('rental_property_detail', kwargs={'pk': self.object.property.pk})
    
    def delete(self, request, *args, **kwargs):
        property_pk = self.get_object().property.pk
        messages.success(request, 'Image deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Function-based views for simpler operations
def set_primary_image(request, pk):
    """Set an image as the primary image for a property"""
    image = get_object_or_404(PropertyImage, pk=pk)
    property = image.property
    
    # Check permissions
    if request.user != property.owner:
        messages.error(request, 'You do not have permission to modify this property.')
        return redirect('rental_property_detail', pk=property.pk)
    
    # Set as primary
    image.is_primary = True
    image.save()  # The save method will handle unsetting other primary images
    
    messages.success(request, 'Primary image updated successfully.')
    return redirect('rental_property_detail', pk=property.pk)


def reorder_images(request, property_pk):
    """Handle AJAX request to reorder images"""
    if request.method == 'POST' and request.is_ajax():
        property = get_object_or_404(RentalProperty, pk=property_pk)
        
        # Check permissions
        if request.user != property.owner:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        # Get the order from the request
        order_data = request.POST.get('order', None)
        if order_data:
            order = json.loads(order_data)
            
            # Update order for each image
            for position, image_id in enumerate(order):
                PropertyImage.objects.filter(id=image_id, property=property).update(display_order=position)
            
            return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


##################################################################################################

from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import RentalProperty, PropertyType
from decimal import Decimal

class PropertyListView(ListView):
    model = RentalProperty
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    paginate_by = 12  # Show 12 properties per page
    
    def get_queryset(self):
        queryset = RentalProperty.objects.all().select_related(
            'property_type', 'region', 'district', 'ward', 'owner'
        ).prefetch_related('images')
        
        # Apply filters based on GET parameters
        
        # Filter by property type
        property_type = self.request.GET.get('property_type')
        if property_type:
            queryset = queryset.filter(property_type_id=property_type)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        if min_price:
            queryset = queryset.filter(monthly_rent__gte=Decimal(min_price))
            
        max_price = self.request.GET.get('max_price')
        if max_price:
            queryset = queryset.filter(monthly_rent__lte=Decimal(max_price))
        
        # Filter by location (city, state, region, district, or ward)
        location = self.request.GET.get('location')
        if location:
            location_query = Q(city__icontains=location) | \
                            Q(state__icontains=location) | \
                            Q(region__name__icontains=location) | \
                            Q(district__name__icontains=location) | \
                            Q(ward__name__icontains=location)
            queryset = queryset.filter(location_query)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add property types for the filter dropdown
        context['property_types'] = PropertyType.objects.all()
        
        # Add status choices for the filter dropdown
        context['status_choices'] = RentalProperty.PROPERTY_STATUS
        
        # Add current filter values to context
        context['selected_type'] = self.request.GET.get('property_type', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['location'] = self.request.GET.get('location', '')
        
        return context


# Add the missing method to the RentalProperty model
# This method should be added to your models.py
def get_primary_image(self):
    """Returns the primary image for this property or None if no images exist."""
    primary_images = self.images.filter(is_primary=True)
    if primary_images.exists():
        return primary_images.first()
    
    # If no primary image is set, return the first image
    if self.images.exists():
        return self.images.first()
    
    return None

# Add this method to your RentalProperty model if it's not already there
RentalProperty.get_primary_image = get_primary_image
#####################################################################################################

from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from .models import RentalProperty, PropertyType, Regions, Districts, Wards

class PropertyListView_out(ListView):
    model = RentalProperty
    template_name = 'property/property_list_out.html'
    context_object_name = 'properties'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(status='available')
        
        # Apply filters from GET parameters
        location = self.request.GET.get('location')
        property_type = self.request.GET.get('property_type')
        price_range = self.request.GET.get('price_range')
        bedrooms = self.request.GET.get('bedrooms')
        
        # Filter by location (region, district, city)
        if location:
            queryset = queryset.filter(
                Q(city__icontains=location) |
                Q(region__rname__icontains=location) |
                Q(district__dname__icontains=location) |
                Q(ward__wname__icontains=location)
            )
        
        # Filter by property type
        if property_type:
            queryset = queryset.filter(property_type_id=property_type)
        
        # Filter by price range
        if price_range:
            if price_range == '0-1000':
                queryset = queryset.filter(monthly_rent__lte=1000)
            elif price_range == '1000-2000':
                queryset = queryset.filter(monthly_rent__gt=1000, monthly_rent__lte=2000)
            elif price_range == '2000-3000':
                queryset = queryset.filter(monthly_rent__gt=2000, monthly_rent__lte=3000)
            elif price_range == '3000+':
                queryset = queryset.filter(monthly_rent__gt=3000)
        
        # Filter by number of bedrooms
        if bedrooms:
            queryset = queryset.filter(number_of_rooms=bedrooms)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add filters to context
        context['property_types'] = PropertyType.objects.all()
        context['regions'] = Regions.objects.all()
        
        # Add selected filter values for form persistence
        context['selected_location'] = self.request.GET.get('location', '')
        context['selected_property_type'] = self.request.GET.get('property_type', '')
        context['selected_price_range'] = self.request.GET.get('price_range', '')
        context['selected_bedrooms'] = self.request.GET.get('bedrooms', '')
        
        # Count properties by type for sidebar
        property_type_counts = {}
        for pt in context['property_types']:
            count = RentalProperty.objects.filter(property_type=pt, status='available').count()
            property_type_counts[pt.id] = count
        context['property_type_counts'] = property_type_counts
        
        # Prepare price ranges for sidebar
        price_ranges = [
            {'label': 'Under $1,000', 'value': '0-1000', 'count': RentalProperty.objects.filter(monthly_rent__lte=1000, status='available').count()},
            {'label': '$1,000 - $2,000', 'value': '1000-2000', 'count': RentalProperty.objects.filter(monthly_rent__gt=1000, monthly_rent__lte=2000, status='available').count()},
            {'label': '$2,000 - $3,000', 'value': '2000-3000', 'count': RentalProperty.objects.filter(monthly_rent__gt=2000, monthly_rent__lte=3000, status='available').count()},
            {'label': 'Over $3,000', 'value': '3000+', 'count': RentalProperty.objects.filter(monthly_rent__gt=3000, status='available').count()},
        ]
        context['price_ranges'] = price_ranges
        
        # Add bedroom options
        bedrooms = [1, 2, 3, 4, 5]
        bedroom_counts = {}
        for br in bedrooms:
            count = RentalProperty.objects.filter(number_of_rooms=br, status='available').count()
            bedroom_counts[br] = count
        context['bedroom_counts'] = bedroom_counts
        
        return context


#########################################################################################

from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import RentalProperty, PropertyType
from decimal import Decimal

class PropertyListView(ListView):
    model = RentalProperty
    template_name = 'property/property_list.html'
    context_object_name = 'properties'
    paginate_by = 12  # Show 12 properties per page
    
    def get_queryset(self):
        queryset = RentalProperty.objects.all().select_related(
            'property_type', 'region', 'district', 'ward', 'owner'
        ).prefetch_related('images')
        
        # Apply filters based on GET parameters
        
        # Filter by property type
        property_type = self.request.GET.get('property_type')
        if property_type:
            queryset = queryset.filter(property_type_id=property_type)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        if min_price:
            queryset = queryset.filter(monthly_rent__gte=Decimal(min_price))
            
        max_price = self.request.GET.get('max_price')
        if max_price:
            queryset = queryset.filter(monthly_rent__lte=Decimal(max_price))
        
        # Filter by location (city, state, region, district, or ward)
        location = self.request.GET.get('location')
        if location:
            location_query = Q(city__icontains=location) | \
                            Q(state__icontains=location) | \
                            Q(region__name__icontains=location) | \
                            Q(district__name__icontains=location) | \
                            Q(ward__name__icontains=location)
            queryset = queryset.filter(location_query)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add property types for the filter dropdown
        context['property_types'] = PropertyType.objects.all()
        
        # Add status choices for the filter dropdown
        context['status_choices'] = RentalProperty.PROPERTY_STATUS
        
        # Add current filter values to context
        context['selected_type'] = self.request.GET.get('property_type', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['location'] = self.request.GET.get('location', '')
        
        return context


# Add the missing method to the RentalProperty model
# This method should be added to your models.py
def get_primary_image(self):
    """Returns the primary image for this property or None if no images exist."""
    primary_images = self.images.filter(is_primary=True)
    if primary_images.exists():
        return primary_images.first()
    
    # If no primary image is set, return the first image
    if self.images.exists():
        return self.images.first()
    
    return None

# Add this method to your RentalProperty model if it's not already there
RentalProperty.get_primary_image = get_primary_image


from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .models import RentalProperty
import logging

# Set up logging
logger = logging.getLogger(__name__)

class PropertyDetailView(DetailView):
    model = RentalProperty
    template_name = 'property/property_detail.html'
    context_object_name = 'property'
    
    def get_object(self, queryset=None):
        """Get the property with related data prefetched."""
        if queryset is None:
            queryset = self.get_queryset()
            
        # Get the property with all related data in a single query
        queryset = queryset.select_related(
            'property_type', 'region', 'district', 'ward', 'owner'
        ).prefetch_related('images')
        
        # Get the object from the filtered queryset
        pk = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(queryset, pk=pk)
    
    def get_context_data(self, **kwargs):
        """Add additional context for administrative divisions."""
        context = super().get_context_data(**kwargs)
        property_obj = context['property']
        
        # Extract ward information
        if property_obj.ward:
            try:
                ward_info = {}
                # Try different attribute names
                if hasattr(property_obj.ward, 'name'):
                    ward_info['name'] = property_obj.ward.name
                elif hasattr(property_obj.ward, 'ward_name'):
                    ward_info['name'] = property_obj.ward.ward_name
                elif hasattr(property_obj.ward, 'title'):
                    ward_info['name'] = property_obj.ward.title
                else:
                    ward_info['name'] = str(property_obj.ward)
                
                context['ward_info'] = ward_info
            except Exception as e:
                logger.error(f"Error extracting ward info: {e}")
                context['ward_info'] = {'name': 'Unknown'}
        
        # Extract district information
        if property_obj.district:
            try:
                district_info = {}
                # Try different attribute names
                if hasattr(property_obj.district, 'name'):
                    district_info['name'] = property_obj.district.name
                elif hasattr(property_obj.district, 'district_name'):
                    district_info['name'] = property_obj.district.district_name
                elif hasattr(property_obj.district, 'title'):
                    district_info['name'] = property_obj.district.title
                else:
                    district_info['name'] = str(property_obj.district)
                
                context['district_info'] = district_info
            except Exception as e:
                logger.error(f"Error extracting district info: {e}")
                context['district_info'] = {'name': 'Unknown'}
        
        # Extract region information
        if property_obj.region:
            try:
                region_info = {}
                # Try different attribute names
                if hasattr(property_obj.region, 'name'):
                    region_info['name'] = property_obj.region.name
                elif hasattr(property_obj.region, 'region_name'):
                    region_info['name'] = property_obj.region.region_name
                elif hasattr(property_obj.region, 'title'):
                    region_info['name'] = property_obj.region.title
                else:
                    region_info['name'] = str(property_obj.region)
                
                context['region_info'] = region_info
            except Exception as e:
                logger.error(f"Error extracting region info: {e}")
                context['region_info'] = {'name': 'Unknown'}
        
        return context

# URL Configuration
"""
# Add to your urls.py:
path('properties/', views.PropertyListView.as_view(), name='property_list'),
path('property/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),

# You'll also want to add these for completeness:
path('property/<int:property_id>/contact/', views.contact_owner, name='contact_owner'),
path('property/<int:property_id>/book/', views.book_property, name='book_property'),
"""

# Additional views for contact and booking (placeholders)
def contact_owner(request, property_id):
    """View to contact property owner."""
    property = get_object_or_404(RentalProperty, id=property_id)
    
    # Placeholder - implement actual contact functionality
    if request.method == 'POST':
        # Process form
        messages.success(request, f"Your message has been sent to the owner of {property.name}.")
        return redirect('property_detail', pk=property_id)
    
    # Show contact form
    context = {
        'property': property
    }
    return render(request, 'property/contact_owner.html', context)

def book_property(request, property_id):
    """View to book a property."""
    property = get_object_or_404(RentalProperty, id=property_id)
    
    # Check if property is available
    if property.status != 'available':
        messages.error(request, f"Sorry, {property.name} is not available for booking at this time.")
        return redirect('property_detail', pk=property_id)
    
    # Placeholder - implement actual booking functionality
    if request.method == 'POST':
        # Process form
        messages.success(request, f"Your booking request for {property.name} has been submitted!")
        return redirect('property_detail', pk=property_id)
    
    # Show booking form
    context = {
        'property': property
    }
    return render(request, 'property/book_property.html', context)






###############################################################################################################################################


from django.views.generic import ListView
from django.db.models import Q
from .models import RentalProperty, PropertyType
from decimal import Decimal

class PropertyTableListView(ListView):
    model = RentalProperty
    template_name = 'property/property_table_list.html'  # Use the table template we created
    context_object_name = 'properties'
    paginate_by = 15  # Show more properties per page in table view
    
    def get_queryset(self):
        queryset = RentalProperty.objects.all().select_related(
            'property_type', 'region', 'district', 'ward', 'owner'
        ).prefetch_related('images')
        
        # Apply filters based on GET parameters
        
        # Filter by property type
        property_type = self.request.GET.get('property_type')
        if property_type:
            queryset = queryset.filter(property_type_id=property_type)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        if min_price:
            queryset = queryset.filter(monthly_rent__gte=Decimal(min_price))
            
        max_price = self.request.GET.get('max_price')
        if max_price:
            queryset = queryset.filter(monthly_rent__lte=Decimal(max_price))
        
        # Filter by location (city, state, region, district, or ward)
        location = self.request.GET.get('location')
        if location:
            location_query = Q(city__icontains=location) | \
                            Q(state__icontains=location)
                            
            # Handle potential missing attributes in location models
            try:
                location_query |= Q(region__name__icontains=location)
            except:
                pass
                
            try:
                location_query |= Q(district__name__icontains=location)
            except:
                pass
                
            try:
                location_query |= Q(ward__name__icontains=location)
            except:
                pass
                
            queryset = queryset.filter(location_query)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add property types for the filter dropdown
        context['property_types'] = PropertyType.objects.all()
        
        # Add status choices for the filter dropdown
        context['status_choices'] = RentalProperty.PROPERTY_STATUS
        
        # Add current filter values to context
        context['selected_type'] = self.request.GET.get('property_type', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['location'] = self.request.GET.get('location', '')
        
        return context
    


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TeamMember
from .forms import TeamMemberForm

def add_team_member(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member added successfully!')
            return redirect('team_list')  # Redirect to a view that lists all team members
    else:
        form = TeamMemberForm()
    
    return render(request, 'add_team_member.html', {'form': form})
    


from django.shortcuts import render
from .models import TeamMember

def team_list(request):
    """View to display all team members."""
    team_members = TeamMember.objects.all().order_by('name')
    context = {
        'team_members': team_members,
        'page_title': 'Our Team'
    }
    return render(request, 'team_list.html', context)


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import TeamMember
from .forms import TeamMemberForm

def edit_team_member(request, member_id):
    """View to edit an existing team member."""
    team_member = get_object_or_404(TeamMember, id=member_id)
    
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=team_member)
        if form.is_valid():
            form.save()
            messages.success(request, f'{team_member.name} updated successfully!')
            return redirect('team_list')
    else:
        form = TeamMemberForm(instance=team_member)
    
    context = {
        'form': form,
        'team_member': team_member,
        'page_title': f'Edit {team_member.name}'
    }
    return render(request, 'edit_team_member.html', context)


# views.py
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import TeamMember

def delete_team_member(request, member_id):
    """View to delete a team member."""
    team_member = get_object_or_404(TeamMember, id=member_id)
    
    # Store the name before deletion for use in success message
    member_name = team_member.name
    
    # Delete the team member
    team_member.delete()
    
    # Add success message
    messages.success(request, f'{member_name} has been removed from the team.')
    
    # Redirect back to the team list
    return redirect('team_list')


def delete_team_member_confirm(request, member_id):
    """View to confirm deletion of a team member."""
    team_member = get_object_or_404(TeamMember, id=member_id)
    
    if request.method == 'POST':
        # Store the name before deletion for use in success message
        member_name = team_member.name
        
        # Delete the team member
        team_member.delete()
        
        # Add success message
        messages.success(request, f'{member_name} has been removed from the team.')
        
        # Redirect back to the team list
        return redirect('team_list')
    
    context = {
        'team_member': team_member,
        'page_title': f'Confirm Delete - {team_member.name}'
    }
    return render(request, 'delete_team_member_confirm.html', context)
#######################################################################################################
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import RentalProperty, PropertyImage, TeamMember

def property_detail_home(request, property_id):
    """
    View for displaying detailed information about a specific rental property.
    """
    # Get the property or return 404 if not found
    property = get_object_or_404(RentalProperty, id=property_id)
    
    # Get all images for this property
    property_images = property.images.all().order_by('display_order', '-is_primary')
    
    # Get property features (can be expanded in the future)
    property_features = {
        'rooms': property.number_of_rooms,
        'bathrooms': getattr(property, 'bathrooms', None),
        'square_feet': getattr(property, 'square_feet', None),
        'parking': getattr(property, 'parking', None),
        'amenities': getattr(property, 'amenities', []),
    }
    
    # Get similar properties (based on type and location)
    similar_properties = RentalProperty.objects.filter(
        property_type=property.property_type,
        status='available'
    ).exclude(id=property.id)[:3]
    
    # Get random agent/team member for contact information
    try:
        agent = TeamMember.objects.order_by('?').first()
    except:
        agent = None
    
    context = {
        'property': property,
        'property_images': property_images,
        'property_features': property_features,
        'similar_properties': similar_properties,
        'agent': agent,
        'google_maps_url': property.get_google_maps_url(),
        'location_hierarchy': property.get_location_hierarchy(),
    }
    
    return render(request, 'property/property_detail_home.html', context)

# Optional: View for handling property inquiries
@login_required
def property_inquiry(request, property_id):
    property = get_object_or_404(RentalProperty, id=property_id)
    
    if request.method == 'POST':
        # Process the inquiry form submission
        # Send email notification, create database record, etc.
        pass
    
    # Redirect back to property detail page
    return redirect('property_detail', property_id=property_id)


############################################################################################################################
from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import RentalProperty, PropertyType
from decimal import Decimal

class PropertyListhomeView(ListView):
    model = RentalProperty
    template_name = 'property/property_list_home.html'
    context_object_name = 'properties'
    paginate_by = 12  # Show 12 properties per page
    
    def get_queryset(self):
        queryset = RentalProperty.objects.all().select_related(
            'property_type', 'region', 'district', 'ward', 'owner'
        ).prefetch_related('images')
        
        # Apply filters based on GET parameters
        
        # Filter by property type
        property_type = self.request.GET.get('property_type')
        if property_type:
            queryset = queryset.filter(property_type_id=property_type)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        if min_price:
            queryset = queryset.filter(monthly_rent__gte=Decimal(min_price))
            
        max_price = self.request.GET.get('max_price')
        if max_price:
            queryset = queryset.filter(monthly_rent__lte=Decimal(max_price))
        
        # Filter by location (city, state, region, district, or ward)
        location = self.request.GET.get('location')
        if location:
            location_query = Q(city__icontains=location) | \
                            Q(state__icontains=location) | \
                            Q(region__name__icontains=location) | \
                            Q(district__name__icontains=location) | \
                            Q(ward__name__icontains=location)
            queryset = queryset.filter(location_query)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add property types for the filter dropdown
        context['property_types'] = PropertyType.objects.all()
        
        # Add status choices for the filter dropdown
        context['status_choices'] = RentalProperty.PROPERTY_STATUS
        
        # Add current filter values to context
        context['selected_type'] = self.request.GET.get('property_type', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['location'] = self.request.GET.get('location', '')
        
        return context


# Add the missing method to the RentalProperty model
# This method should be added to your models.py
def get_primary_image(self):
    """Returns the primary image for this property or None if no images exist."""
    primary_images = self.images.filter(is_primary=True)
    if primary_images.exists():
        return primary_images.first()
    
    # If no primary image is set, return the first image
    if self.images.exists():
        return self.images.first()
    
    return None

# Add this method to your RentalProperty model if it's not already there
RentalProperty.get_primary_image = get_primary_image

