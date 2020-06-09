import json

from django import template
import urllib

from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.urls import reverse_lazy, reverse
from django.utils.safestring import mark_safe

from app.models import DocumentFile, Batch, STAGES, BATCH, STATES

register = template.Library()

ACTIONS = ['Open', 'Done', 'Continue_Editing', 'Close']
ACTIONS_STAGE = ['Dispatch to Reception',
                 'Return to Registry', 'Dispatch to Assembler',
                 'Return to Reception', 'Dispatch to Scanner',
                 'Dispatch to Transcriber',
                 'Return to Scanner', 'Dispatch to QA',
                 'Return to Transcriber', 'Dispatch to Validator',
                 'Return to QA', 'Fully Digitized']


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
    if len(transitions) > 1:
        for transition in transitions:
            if transition.target == BATCH[0] or transition.target == BATCH[2]:
                return format_html(u'<div role="separator" class="dropdown-divider"></div><div class="dropdown-item '
                                   u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                                   u'}">Continue editing</a></div><div role="separator" '
                                   u'class="dropdown-divider"></div><div class="dropdown-item '
                                   u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                                   u'}">Close</a></div>',
                                   reverse_lazy('update_state_batch', args=[id, ACTIONS[2]]),
                                   reverse_lazy('update_state_batch', args=[id, ACTIONS[3]]))
            get_actions_batch.allow_tags = True
    else:
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
    stage_transitions = list(file.get_available_stage_transitions())

    if len(stage_transitions) > 1:
        print(
            f'{stage_transitions[0].source} {STAGES.index(stage_transitions[0].source)} to {stage_transitions[0].target} {STAGES.index(stage_transitions[0].target)} ')
        print(
            f'{stage_transitions[1].source} {STAGES.index(stage_transitions[1].source)} to {stage_transitions[1].target} {STAGES.index(stage_transitions[1].target)} ')

        if stage_transitions[0].target == STAGES[2] and stage_transitions[1].target == STAGES[0]:
            return format_html(u'<div role="separator" class="dropdown-divider"></div><div class="dropdown-item '
                               u'btn btn-info btn-block"><button class="dropdown-item return btn btn-info btn-block" id="{}"  data-toggle="modal" data-target="#modal-lg">Return Registry</button></div><div role="separator" '
                               u'class="dropdown-divider"></div><div class="dropdown-item '
                               u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                               u'}">Dispatch To Assembly</a></div>',
                               reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[1]]),
                               reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[2]]))
        if stage_transitions[0].target == STAGES[3] and stage_transitions[1].target == STAGES[1]:
            return format_html(u'<div role="separator" class="dropdown-divider"></div><div class="dropdown-item '
                               u'btn btn-info btn-block"><button class="dropdown-item return btn btn-info btn-block" id="{}"  data-toggle="modal" data-target="#modal-lg">Return Reception</button></div><div role="separator" '
                               u'class="dropdown-divider"></div><div class="dropdown-item '
                               u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                               u'}">Dispatch To Scanner</a></div>',
                               reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[3]]),
                               reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[4]]))
        if stage_transitions[0].target == STAGES[5] and stage_transitions[1].target == STAGES[3]:
            return format_html(u'<div role="separator" class="dropdown-divider"></div><div class="dropdown-item '
                               u'btn btn-info btn-block"><button class="dropdown-item return btn btn-info btn-block" id="{}"  data-toggle="modal" data-target="#modal-lg">Return To Scanner</button></div><div role="separator" '
                               u'class="dropdown-divider"></div><div class="dropdown-item '
                               u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                               u'}">Dispatch To QA</a></div>',
                               reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[6]]),
                               reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[7]]))
        if stage_transitions[0].target == STAGES[6] and stage_transitions[1].target == STAGES[4]:
            return format_html(u'<div role="separator" class="dropdown-divider"></div><div class="dropdown-item '
                               u'btn btn-info btn-block"><button class="dropdown-item return btn btn-info btn-block" '
                               u'id="{}"  data-toggle="modal" data-target="#modal-lg">Return To '
                               u'Transacriber</button></div><div role="separator" '
                               u'class="dropdown-divider"></div><div class="dropdown-item '
                               u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                               u'}">Dispatch To Validator</a></div>',
                               reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[8]]),
                               reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[9]]))

        if stage_transitions[0].target == STAGES[7] and stage_transitions[1].target == STAGES[5]:
            return format_html(u'<div role="separator" class="dropdown-divider"></div><div class="dropdown-item '
                               u'btn btn-info btn-block"><button class="dropdown-item return btn btn-info btn-block" '
                               u'id="{}"  data-toggle="modal" data-target="#modal-lg">Return To QA</button></div><div '
                               u'role="separator" '
                               u'class="dropdown-divider"></div><div class="dropdown-item '
                               u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                               u'}">Mark as Complete</a></div>',
                               reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[10]]),
                               reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[11]]))
    else:
        for transition in stage_transitions:

            if transition.source == STAGES[0] and transition.target == STAGES[1]:
                return format_html(u'<div role="separator" '
                                   u'class="dropdown-divider"></div><div class="dropdown-item '
                                   u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                                   u'}">Send To Reception</a></div>',
                                   reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[0]]))

            if transition.source == STAGES[3] and transition.target == STAGES[4]:
                return format_html(u'<div role="separator" '
                                   u'class="dropdown-divider"></div><div class="dropdown-item '
                                   u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                                   u'}">Send To Transcriber</a></div>',
                                   reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[5]]))


@register.filter
def get_actions_file_state(id):
    file = DocumentFile.objects.get(pk=id)
    transitions = list(file.get_available_state_transitions())
    if len(transitions) > 1:
        for transition in transitions:
            if transition.target == STATES[0] or transition.target == STATES[2]:
                return format_html(u'<div role="separator" class="dropdown-divider"></div><div class="dropdown-item '
                                   u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                                   u'}">Continue editing</a></div><div role="separator" '
                                   u'class="dropdown-divider"></div><div class="dropdown-item '
                                   u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                                   u'}">Close</a></div>',
                                   reverse_lazy('update_state_file', args=[id, ACTIONS[2]]),
                                   reverse_lazy('update_state_file', args=[id, ACTIONS[3]]))
    else:
        for transition in transitions:
            print(f'file transition source={transition.source}')
            print(f'file transition target={transition.target}')
            if transition.source == STATES[0] and transition.target == STATES[1]:
                return format_html(u'<div role="separator" '
                                   u'class="dropdown-divider"></div><div class="dropdown-item '
                                   u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                                   u'}">Done Editing</a></div>',
                                   reverse_lazy('update_state_file', args=[id, ACTIONS[1]]))
            if transition.source == STATES[1] and transition.target == STATES[0]:
                return format_html(u'<div role="separator" '
                                   u'class="dropdown-divider"></div><div class="dropdown-item '
                                   u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                                   u'}">Continue  Editing</a></div>',
                                   reverse_lazy('update_state_file', args=[id, ACTIONS[2]]))
            if transition.source == STATES[1] and transition.target == STATES[2]:
                return format_html(u'<div role="separator" '
                                   u'class="dropdown-divider"></div><div class="dropdown-item '
                                   u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                                   u'}">Close</a></div>',
                                   reverse_lazy('update_state_file', args=[id, ACTIONS[3]]))
            if transition.source == STATES[2] and transition.target == STATES[0]:
                return format_html(u'<div role="separator" '
                                   u'class="dropdown-divider"></div><div class="dropdown-item '
                                   u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                                   u'}">Re-Open</a></div>',
                                   reverse_lazy('update_state_file', args=[id, ACTIONS[0]]))
            get_actions_batch.allow_tags = True


@register.filter
def get_validate_buttons(id):
    file = DocumentFile.objects.get(pk=id)
    stage_transitions = list(file.get_available_stage_transitions())
    if file.stage == STAGES[6]:
            return format_html(u'<div role="separator" class="dropdown-divider"></div><div class="dropdown-item '
                               u'btn btn-info btn-block"><button class="dropdown-item return btn btn-info btn-block" '
                               u'id="{}"  data-toggle="modal" data-target="#modal-lg">Return To QA</button></div><div '
                               u'role="separator" '
                               u'class="dropdown-divider"></div><div class="dropdown-item '
                               u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                               u'}">Finalize to Reception</a></div>',
                               reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[10]]),
                               reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[11]]))



@register.filter
def get_qa_buttons(id):
    file = DocumentFile.objects.get(pk=id)
    stage_transitions = list(file.get_available_stage_transitions())
    if file.stage == STAGES[5]:
        return format_html(u'<div role="separator" class="dropdown-divider"></div><div class="dropdown-item '
                           u'btn btn-info btn-block"><button class="dropdown-item return btn btn-info btn-block" '
                           u'id="{}"  data-toggle="modal" data-target="#modal-lg">Return To '
                           u'Transcriber</button></div><div role="separator" '
                           u'class="dropdown-divider"></div><div class="dropdown-item '
                           u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                           u'}">Dispatch To Validator</a></div>',
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[8]]),
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[9]]))
    elif file.stage == STAGES[6]:
        return format_html(u'<div role="separator" class="dropdown-divider"></div><div class="dropdown-item '
                           u'btn btn-info btn-block"><button class="dropdown-item return btn btn-info btn-block" '
                           u'id="{}"  data-toggle="modal" data-target="#modal-lg">Return To '
                           u'Transcriber</button></div><div role="separator" '
                           u'class="dropdown-divider"></div><div class="dropdown-item '
                           u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                           u'}">Return To Registry</a></div>',
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[8]]),
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[11]]))


@register.filter
def get_receiver_buttons(id):
    file = DocumentFile.objects.get(pk=id)
    stage_transitions = list(file.get_available_stage_transitions())
    if file.stage == STAGES[1]:
        return format_html(u'<div role="separator" class="dropdown-divider"></div><div class="dropdown-item '
                           u'btn btn-info btn-block"><button class="dropdown-item return btn btn-info btn-block" '
                           u'id="{}"  data-toggle="modal" data-target="#modal-lg">Return To '
                           u'Return Registry</button></div><div role="separator" '
                           u'class="dropdown-divider"></div><div class="dropdown-item '
                           u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                           u'}">Dispatch To Assembler</a></div>',
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[8]]),
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[9]]))

@register.filter
def get_assembler_buttons(id):
    file = DocumentFile.objects.get(pk=id)
    stage_transitions = list(file.get_available_stage_transitions())
    if file.stage == STAGES[5]:
        return format_html(u'<div role="separator" class="dropdown-divider"></div><div class="dropdown-item '
                           u'btn btn-info btn-block"><button class="dropdown-item return btn btn-info btn-block" '
                           u'id="{}"  data-toggle="modal" data-target="#modal-lg">Return To '
                           u'Return Registry</button></div><div role="separator" '
                           u'class="dropdown-divider"></div><div class="dropdown-item '
                           u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                           u'}">Dispatch To Assembler</a></div>',
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[8]]),
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[9]]))

@register.filter
def get_receiver_actions(id):
    file = DocumentFile.objects.get(pk=id)
    stage_transitions = list(file.get_available_stage_transitions())
    if file.stage == STAGES[5]:
        return format_html(u'<div role="separator" class="dropdown-divider"></div><div class="dropdown-item '
                           u'btn btn-info btn-block"><button class="dropdown-item return btn btn-info btn-block" '
                           u'id="{}"  data-toggle="modal" data-target="#modal-lg">Return To '
                           u'Return Registry</button></div><div role="separator" '
                           u'class="dropdown-divider"></div><div class="dropdown-item '
                           u'btn btn-info btn-block"><a class="dropdown-item btn btn-info btn-block" href="{'
                           u'}">Accept</a></div>',
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[8]]),
                           reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[9]]))

@register.filter
def dispatch_to_transcriber(id):
    return format_html(u'<a class="btn btn-info btn-block" href="{}">Dispatch To Transcriber</a>',
                       reverse_lazy('update_stage_file', args=[id, ACTIONS_STAGE[5]]))


@register.filter
def preview_document(url):
    return format_html(u'<embed id="pdf" src="{}"  width= "100%" height= "800">')


@register.filter
def clean_json(data):
    return json.dumps(data)