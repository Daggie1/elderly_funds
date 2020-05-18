from django import template
import urllib

register = template.Library()


@register.filter
def concat_string(value_1, value_2):
    # parse this strings into a url
    value_2 = urllib.parse.quote(value_2)
    value_1 = 'http://' + str(value_1)
    return str(value_1) + str('/media/') +str(value_2)

@register.filter
def get_fields(obj):
    print(obj)
    # return [(field.name, field.value_to_string(obj)) for field in obj._meta.fields]
    return "nothing"

@register.filter
def get_actions(obj):
    pass