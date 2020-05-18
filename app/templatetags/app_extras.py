from django import template
import urllib

register = template.Library()


@register.filter
def concat_string(value_1, value_2):
    # parse this strings into a url
    value_2 = urllib.parse.quote(value_2)
    value_1 = 'http://' + str(value_1)
    return str(value_1) + str('/media/') +str(value_2)

