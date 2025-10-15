from django import template
from django.utils import translation
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def get_translated_field(obj, field_name, language=None):
    """
    Get the translated value of a model field based on the current language.
    This is a custom implementation since modeltranslation is not working.
    """
    if language is None:
        language = translation.get_language()
    
    # For now, just return the original field value
    # In a real implementation, you would check for translated fields
    # like field_name_uz, field_name_ru, field_name_uz_cyrl
    return getattr(obj, field_name, '')

@register.simple_tag
def get_translated_choice(obj, field_name, language=None):
    """
    Get the translated choice value for a model field.
    """
    if language is None:
        language = translation.get_language()
    
    # Get the choice value
    choice_value = getattr(obj, field_name, '')
    
    # Get the choice display
    choice_display = getattr(obj, f'get_{field_name}_display', lambda: choice_value)()
    
    return choice_display

@register.simple_tag
def get_translated_related_field(obj, field_name, related_field, language=None):
    """
    Get the translated value of a related model field.
    """
    if language is None:
        language = translation.get_language()
    
    try:
        related_obj = getattr(obj, field_name)
        if related_obj:
            return getattr(related_obj, related_field, '')
    except:
        pass
    
    return ''
