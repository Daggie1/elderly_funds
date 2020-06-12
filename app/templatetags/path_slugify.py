from django import template

register = template.Library()

@register.filter
def clean_path(path):
    return path.replace("\\",'-')