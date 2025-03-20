# Add this to your project's templatetags directory
# e.g., yourapp/templatetags/form_tags.py

from django import template
from django.template.defaultfilters import safe

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='render_field')
def render_field(field):
    """Renders a field with its widget and any attributes already set in the form"""
    return safe(field)