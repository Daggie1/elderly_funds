from django import template
import urllib

from django.utils.html import format_html
from django.urls import reverse_lazy

from app.models import DocumentFile, Batch, STAGES,BATCH

register = template.Library()

ACTIONS = ['Open', 'Done', 'Continue_Editing', 'Close']
ACTIONS_STAGE = ['Dispatch to Reception',
                 'Return to Registry', 'Dispatch to Assembler', 'Return to Reception', 'Dispatch to Scanner',
                 'Dispatch to Transcriber',
                 'Dispatch to QA',
                 'Dispatch to Validator',
                 'Finalize to Reception']




@register.filter
def concat_string(value_1, value_2):
    # parse this strings into a url
    value_2 = urllib.parse.quote(value_2)
    value_1 = 'http://' + str(value_1)
    return str(value_1) + str('/media/') + str(value_2)


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
    for transition in transitions:
        print(f'batch transition source={transition.source}')
        print(f'batch transition target={transition.target}')
        if transition.source == BATCH[0] and transition.target == BATCH[1]:
            return format_html(u'<a class="dropdown-item btn btn-info btn-block" href="{}">Done Editing</a>',
                               reverse_lazy('update_state_batch', args=[id, ACTIONS[1]]))
        if transition.source == BATCH[1] and transition.target == BATCH[0]:
            return format_html(u'<a class="dropdown-item btn btn-info btn-block" href="{}">Continue Editing</a>',
                               reverse_lazy('update_state_batch', args=[id, ACTIONS[2]]))
        if transition.source == BATCH[1] and transition.target == BATCH[2]:
            return format_html(u'<a class="dropdown-item btn btn-info btn-block" href="{}">Close(Complete)</a>',
                               reverse_lazy('update_state_batch', args=[id, ACTIONS[3]]))
        get_actions_batch.allow_tags = True


@register.filter
def get_actions_file(id):
    file = DocumentFile.objects.get(pk=id)
    transitions = list(file.get_available_state_transitions())
    stage_transitions = list(file.get_available_stage_transitions())

    print(f'file={file}stage_transitions={stage_transitions}')
    for transition in stage_transitions:
        print(f'transition source={transition.source}')
        print(f'transition target={transition.target}')
        if transition.source== STAGES[0] and transition.target == STAGES[1] :
            return format_html(u'<a class="dropdown-item btn btn-info btn-block" href="{}">Send To Reception</a>',
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[0]]))
        if transition.source== STAGES[1] and transition.target == STAGES[0]:
            return format_html(u'<a class="dropdown-item btn btn-info btn-block" href="{}">Return To Registry</a>',
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[1]]))
        if transition.source== STAGES[1] and transition.target == STAGES[2]:
            return format_html(u'<a class="dropdown-item btn btn-info btn-block" href="{}">Send To Assembler</a>',
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[2]]))
        if transition.source== STAGES[2] and transition.target == STAGES[1]:
            return format_html(u'<a class="dropdown-item btn btn-info btn-block" href="{}">Return To Reception</a>',
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[3]]))
        if transition.source== STAGES[2] and transition.target == STAGES[3]:
            return format_html(u'<a class="dropdown-item btn btn-info btn-block" href="{}">Send To Scanner</a>',
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[4]]))
        if transition.source== STAGES[3] and transition.target == STAGES[4]:
            return format_html(u'<a class="dropdown-item btn btn-info btn-block" href="{}">Send To Transcriber</a>',
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[5]]))
        if transition.source== STAGES[4] and transition.target == STAGES[5]:
            return format_html(u'<a class="dropdown-item btn btn-info btn-block" href="{}">Send to QA</a>',
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[6]]))
        if transition.source== STAGES[5] and transition.target == STAGES[6]:
            return format_html(u'<a class="dropdown-item btn btn-info btn-block" href="{}">Send To Validator</a>',
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[7]]))
        if transition.source== STAGES[6] and transition.target == STAGES[7]:
            return format_html(u'<a class="dropdown-item btn btn-info btn-block" href="{}">Finalize To Reception</a>',
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[8]]))


