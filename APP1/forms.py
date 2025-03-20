# APP1/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class RentalLoginForm(forms.Form):
    """
    Enhanced login form with additional security features
    """
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
                'autocomplete': 'email',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password',
                'autocomplete': 'current-password',
            }
        )
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower() if email else None
        return email
from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
import json

User = get_user_model()
 
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    profile_pic = forms.ImageField(required=False)  # Keep this as ImageField for form validation
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'profile_pic']
        # Note: 'profile_pic' is here for the form but model will use profile_pic_data & profile_pic_type
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add the form-control class to all fields
        for field_name, field in self.fields.items():
            # Don't add form-control to the profile_pic field or the hidden role field
            if field_name not in ['profile_pic', 'role']:
                field.widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match."
            )
        return cleaned_data
    
class ProfileForm(forms.ModelForm):
    """
    Form for additional profile fields that change based on user role
    """
    class Meta:
        from .models import Profile
        model = Profile
        fields = ['phone_number', 'address']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address',
                'rows': 3
            })
        }
    
    def __init__(self, *args, **kwargs):
        # Get user role to customize fields
        self.user_role = kwargs.pop('user_role', None)
        super().__init__(*args, **kwargs)
        
        # Add role-specific fields
        if self.user_role == 'landlord':
            self.fields['company_name'] = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your company name (optional)'
                })
            )
        
        elif self.user_role == 'agent':
            self.fields['license_number'] = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your license number (optional)'
                })
            )
        
        elif self.user_role == 'tenant':
            self.fields['preferred_location'] = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your preferred location (optional)'
                })
            )
            self.fields['max_budget'] = forms.DecimalField(
                required=False,
                widget=forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your maximum budget (optional)'
                })
            )

class ProfileUpdateForm(forms.Form):
    """
    Form for updating user profile information
    """
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    profile_pic = forms.ImageField(required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    is_landlord = forms.BooleanField(required=False)




    #######################################################################################################################################################################################################
from django import forms
from .models import Location, Regions, Districts, Wards

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            'name', 
            'address', 
            'region',
            'district',
            'ward',
            'city', 
            'zip_code', 
            'country', 
            'latitude', 
            'longitude', 
            'description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control', 'id': 'region-select'}),
            'district': forms.Select(attrs={'class': 'form-control', 'id': 'district-select'}),
            'ward': forms.Select(attrs={'class': 'form-control', 'id': 'ward-select'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001', 'id': 'id_latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001', 'id': 'id_longitude'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = Districts.objects.none()
        self.fields['ward'].queryset = Wards.objects.none()
        
        # If form is being edited and has region selected
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['district'].queryset = Districts.objects.filter(mkoa_id=region_id).order_by('dname')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.region:
            self.fields['district'].queryset = Districts.objects.filter(mkoa_id=self.instance.region).order_by('dname')
            
        # If form is being edited and has district selected
        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['ward'].queryset = Wards.objects.filter(wilaya=district_id).order_by('wname')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.district:
            self.fields['ward'].queryset = Wards.objects.filter(wilaya=self.instance.district).order_by('wname')  
####################################################################################################################################################################
from django import forms
from django.utils.translation import gettext_lazy as _

from django import forms
from .models import PropertyType, RentalProperty, PropertyImage

class PropertyTypeForm(forms.ModelForm):
    """Form for creating and updating property types"""
    
    class Meta:
        model = PropertyType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter property type name',
                'autocomplete': 'off',
                'aria-describedby': 'nameHelp'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter property type description',
                'aria-describedby': 'descriptionHelp'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control class to all fields by default
        for field_name, field in self.fields.items():
            # Add help text for better user guidance
            if field_name == 'name':
                field.help_text = 'Enter a unique and descriptive name for this property type'
            elif field_name == 'description':
                field.help_text = 'Provide details about what makes this property type distinct'
                
            # Set all fields as required by default
            field.required = True
            
            # Add validation classes for Bootstrap
            css_classes = field.widget.attrs.get('class', '')
            if 'form-control' not in css_classes:
                field.widget.attrs['class'] = f'{css_classes} form-control'
                

class RentalPropertyForm(forms.ModelForm):
    """Form for creating and updating rental properties"""
    
    class Meta:
        model = RentalProperty
        fields = [
            'name', 'property_type', 'address', 'city', 'state', 'zip_code',
            'latitude', 'longitude', 'place_id', 'region', 'district', 'ward',
            'number_of_rooms', 'monthly_rent', 'status'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'monthly_rent': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'latitude': forms.NumberInput(attrs={'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'step': 'any'}),
        }
        help_texts = {
            'place_id': _('Google Maps Place ID for location integration'),
            'latitude': _('Decimal coordinates (e.g., 37.7749)'),
            'longitude': _('Decimal coordinates (e.g., -122.4194)'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Make some fields optional
        for field in ['latitude', 'longitude', 'place_id', 'region', 'district', 'ward']:
            self.fields[field].required = False


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'title', 'alt_text', 'description', 'category', 'is_primary', 'display_order']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field in self.fields:
            if field != 'is_primary':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Optional fields
        for field in ['title', 'alt_text', 'description', 'category', 'display_order']:
            self.fields[field].required = False



from django import forms
from .models import TeamMember

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'image', 'linkedin', 'twitter', 'facebook']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/username'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/username'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/username'}),
        }