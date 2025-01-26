from django import forms
from .models import Student
from django.core.validators import RegexValidator

class DataForm(forms.ModelForm):
        regno=forms.CharField(label='Index/AVN number',min_length=3,max_length=50,validators=[RegexValidator(r'^[a-zA-Z@.]*$',message="Index/AVN number")],widget=forms.TextInput(attrs={'placeholder':'example S/2021/009'}))
      
        class Meta:
         model = Student
         fields = "__all__"
 


from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)