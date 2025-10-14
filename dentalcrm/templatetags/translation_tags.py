"""
Custom template tags for translation support.
"""
from django import template
from django.utils.translation import get_language
from dentalcrm.translations import get_translation

register = template.Library()

@register.filter
def translate(text):
    """
    Custom template filter to translate text based on current language.
    Usage: {{ "Hello"|translate }}
    """
    current_language = get_language()
    return get_translation(text, current_language)

@register.simple_tag
def trans(text):
    """
    Custom template tag to translate text.
    Usage: {% trans "Hello" %}
    """
    current_language = get_language()
    return get_translation(text, current_language)
