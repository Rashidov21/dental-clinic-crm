"""
Custom template tags for translation support.
"""
from django import template
from dentalcrm.translations import get_translation

register = template.Library()

@register.filter
def translate(text):
    """
    Custom template filter to translate text based on current language.
    Usage: {{ "Hello"|translate }}
    """
    return get_translation(text, 'uz')  # Default to Uzbek Latin

@register.simple_tag(takes_context=True)
def trans(context, text):
    """
    Custom template tag to translate text.
    Usage: {% trans "Hello" %}
    """
    # Get language from session, default to 'uz'
    current_language = context['request'].session.get('django_language', 'uz')
    return get_translation(text, current_language)
