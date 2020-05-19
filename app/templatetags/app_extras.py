from django import template
import urllib

from django.utils.html import format_html
from django.urls import reverse_lazy

from app.models import DocumentFile, Batch, DocumentFileDetail
register = template.Library()
ACTIONS=['Open','Done','Continue_Editing','Close']

@register.filter
def concat_string(value_1, value_2):
    # parse this strings into a url
    value_2 = urllib.parse.quote(value_2)
    value_1 = 'http://' + str(value_1)
    return str(value_1) + str('/media/') +str(value_2)

@register.filter
def get_fields(obj):
    # print(dir(obj))
    print(obj.__dict__)
    print(obj.data.__dict__)
    # return [(field.name, field.value_to_string(obj)) for field in obj._meta.fields]
    return "nothing"

@register.filter
def get_actions_batch(id):
    batch = Batch.objects.get(pk=id)
    transitions = list(batch.get_available_state_transitions())
    # stage_transitions = list(batch.get_available_stage_transitions())

    if transitions[0].target == "Done":
        return format_html(u'<a class="dropdown-item btn btn-info btn-block" href="{}">Mark As Complete</a>', reverse_lazy('update_state_batch',args=[id, ACTIONS[1]]))
    get_actions_batch.allow_tags = True

@register.filter
def get_actions_file(id):
    file = DocumentFile.objects.get(pk=id)
    transitions = list(file.get_available_state_transitions())
    stage_transitions = list(file.get_available_stage_transitions())
    if stage_transitions[0].target == "Reception":
        return format_html(u'<a class="dropdown-item btn btn-info btn-block" href="{}">Send To Reception</a>', reverse_lazy('update_stage_file',args=[id, ACTIONS[1]]))
