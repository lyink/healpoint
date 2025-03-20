# APP1/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import base64
from io import BytesIO
from PIL import Image

# Define UserManager first
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)

# Define User model
class User(AbstractBaseUser, PermissionsMixin):
    # Updated role choices to match template
    ROLE_CHOICES = [
        ('landlord', 'Landlord'),
        ('agent', 'Agent'),
        ('tenant', 'Tenant'),
    ]
        
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    profile_pic_data = models.BinaryField(null=True, blank=True)
    profile_pic_type = models.CharField(max_length=20, null=True, blank=True)  # Store the image MIME type
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='tenant')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def get_profile_pic_base64(self):
        """Returns the profile picture as a base64 encoded string for display in templates"""
        if self.profile_pic_data:
            return f"data:{self.profile_pic_type};base64,{base64.b64encode(self.profile_pic_data).decode('utf-8')}"
        return None
    
    def set_profile_pic(self, image_file):
        """Process and save the profile picture as binary data"""
        if image_file:
            # Get file extension and determine MIME type
            file_ext = image_file.name.split('.')[-1].lower()
            mime_types = {
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png'
            }
            
            if file_ext not in mime_types:
                raise ValueError('Invalid file type. Only JPG, JPEG, and PNG files are allowed.')
            
            # Use PIL to process the image
            img = Image.open(image_file)
            
            # Optional: resize the image to save space
            # img.thumbnail((800, 800))
            
            # Convert to binary data
            buffer = BytesIO()
            # Use a standardized format name that PIL recognizes
            format_map = {
                'jpg': 'JPEG',
                'jpeg': 'JPEG',
                'png': 'PNG'
            }
            img.save(buffer, format=format_map.get(file_ext, 'JPEG'))
            
            # Store in model fields
            self.profile_pic_data = buffer.getvalue()
            self.profile_pic_type = mime_types[file_ext]

# Define Profile model with additional fields for each role type
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Fields for landlords
    company_name = models.CharField(max_length=255, blank=True, null=True)
    
    # Fields for agents
    license_number = models.CharField(max_length=100, blank=True, null=True)
    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='managed_agents'
    )
    
    # Fields for tenants
    preferred_location = models.CharField(max_length=255, blank=True, null=True)
    max_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

# Model for agent invitations
class AgentInvitation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    
    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='sent_invitations'
    )
    email = models.EmailField()
    token = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Invitation from {self.landlord.username} to {self.email}"
class Property(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'property')
    
    def __str__(self):
        return f"{self.user.username} - {self.property.title}"

class PropertyView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='property_views')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} viewed {self.property.title}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.property.title} - {self.date}"

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}"

class Activity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.description}"
    
############################################################################################################################################################
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Regions(models.Model):
    rname = models.CharField(max_length=100, verbose_name="Region Name")
    code = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return self.rname
    
    class Meta:
        ordering = ['rname']

class Districts(models.Model):
    dname = models.CharField(max_length=150, verbose_name="District Name")
    mkoa_id = models.ForeignKey(Regions, on_delete=models.CASCADE, verbose_name="Region")
    
    def __str__(self):
        return f"{self.dname} - {self.mkoa_id.rname}"
    
    class Meta:
        ordering = ['dname']

class Wards(models.Model):
    wname = models.CharField(max_length=150, verbose_name="Ward Name")
    wilaya = models.ForeignKey(Districts, on_delete=models.CASCADE, verbose_name="District")
    
    def __str__(self):
        return f"{self.wname} - {self.wilaya.dname}"
    
    class Meta:
        ordering = ['wname']

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    region = models.ForeignKey(Regions, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(Districts, on_delete=models.SET_NULL, null=True, blank=True)
    ward = models.ForeignKey(Wards, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default="Tanzania")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
                                  validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
                                   validators=[MinValueValidator(-180), MaxValueValidator(180)])
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('location_detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['name']

#####################################################################################################
from django.db import models

class PropertyType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class RentalProperty(models.Model):
    PROPERTY_STATUS = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('under_maintenance', 'Under Maintenance'),
    )
    name = models.CharField(max_length=255)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    
    # Google location fields
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    place_id = models.CharField(max_length=255, null=True, blank=True, help_text="Google Maps Place ID")
    
    # Administrative divisions
    region = models.ForeignKey(Regions, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(Districts, on_delete=models.SET_NULL, null=True, blank=True)
    ward = models.ForeignKey(Wards, on_delete=models.SET_NULL, null=True, blank=True)
    
    number_of_rooms = models.IntegerField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PROPERTY_STATUS, default='available')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_properties')

    def __str__(self):
        return f"{self.name} - {self.address}"
    
    def get_google_maps_url(self):
        """
        Returns a Google Maps URL for this property if latitude and longitude are available.
        """
        if self.latitude and self.longitude:
            return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
        return None
    
    def get_location_hierarchy(self):
        """
        Returns a string representing the full administrative hierarchy of the property location.
        """
        location_parts = []
        if self.ward:
            location_parts.append(self.ward.wname)
        if self.district:
            location_parts.append(self.district.dname)
        if self.region:
            location_parts.append(self.region.rname)
        
        return " > ".join(location_parts) if location_parts else "Location hierarchy not set"
    

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import os

class PropertyImage(models.Model):
    """
    Model for storing property images with associated metadata.
    Each property can have multiple images.
    """
    
    # Relationship to Property model
    property = models.ForeignKey(
        'RentalProperty',  # Using string to avoid import cycles
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_("Property")
    )
    
    # Image file
    image = models.ImageField(
        upload_to='property_images/%Y/%m/',
        verbose_name=_("Image")
    )
    
    # Metadata fields
    title = models.CharField(
        max_length=255, 
        blank=True, 
        verbose_name=_("Title")
    )
    
    alt_text = models.CharField(
        max_length=255, 
        blank=True,
        help_text=_("Alternative text for accessibility"),
        verbose_name=_("Alt Text")
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_("Primary Image"),
        help_text=_("Set as the main image for this property")
    )
    
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Display Order"),
        help_text=_("Order in which images are displayed (lowest first)")
    )
    
    uploaded_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Uploaded At")
    )
    
    # Optional image category/tag
    category = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('exterior', _('Exterior')),
            ('interior', _('Interior')),
            ('kitchen', _('Kitchen')),
            ('bathroom', _('Bathroom')),
            ('bedroom', _('Bedroom')),
            ('living_area', _('Living Area')),
            ('view', _('View')),
            ('other', _('Other')),
        ],
        verbose_name=_("Category")
    )
    
    # Meta options
    class Meta:
        verbose_name = _("Property Image")
        verbose_name_plural = _("Property Images")
        ordering = ['display_order', 'uploaded_at']
    
    def __str__(self):
        """String representation of the property image."""
        if self.title:
            return f"{self.title} - {self.property.name}"
        return f"Image for {self.property.name}"
    
    def save(self, *args, **kwargs):
        """
        Override save method to ensure only one primary image per property.
        If this image is set as primary, unset any other primary images.
        """
        if self.is_primary:
            # Set all other images of this property to not primary
            PropertyImage.objects.filter(
                property=self.property, 
                is_primary=True
            ).exclude(
                id=self.id
            ).update(is_primary=False)
        
        super().save(*args, **kwargs)
    
    def get_filename(self):
        """Return the filename of the image."""
        return os.path.basename(self.image.name)
    
    def delete(self, *args, **kwargs):
        """
        Override delete method to delete the image file from storage.
        """
        # Store the path to delete after the model instance is deleted
        storage, path = self.image.storage, self.image.path
        
        # Delete the model instance
        super().delete(*args, **kwargs)
        
        # Delete the file after the model instance is deleted
        storage.delete(path)

def get_primary_image(self):
    """Returns the primary image for this property or None if no images exist."""
    primary_images = self.images.filter(is_primary=True)
    if primary_images.exists():
        return primary_images.first()
    return None


##################################################################################################################
from django.db import models
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team_images/')
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    def str(self):
        return self.name

# In your views.py
def get_profile_pic_url(self):
    if self.profile_pic_data and self.profile_pic_type:
        return f"data:{self.profile_pic_type};base64,{base64.b64encode(self.profile_pic_data).decode('utf-8')}"
    return None

###########################################################################################################################
# Add this method to your RentalProperty model

def get_primary_image(self):
    """Returns the primary image for this property or the first image if no primary is set."""
    primary_images = self.images.filter(is_primary=True)
    if primary_images.exists():
        return primary_images.first()
    # If no primary image is set, return the first image
    if self.images.exists():
        return self.images.first()
    return None

# Additional helpful properties you can add to the RentalProperty model

@property
def bathrooms(self):
    """Get bathrooms count from related property details if it exists."""
    if hasattr(self, 'property_details'):
        return getattr(self.property_details, 'bathrooms', None)
    return None

@property
def square_feet(self):
    """Get square footage from related property details if it exists."""
    if hasattr(self, 'property_details'):
        return getattr(self.property_details, 'square_feet', None)
    return None

@property
def is_available(self):
    """Check if property is available for rent."""
    return self.status == 'available'