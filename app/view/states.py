from app.models import *

""" this module manages the document workflow and states of individual objects """
""":key primary key"""
""":keyword batch"""
""":keyword file"""
""":keyword document"""

stages = [
    'registry',
    'reception',
    'disassembly',
    'scanning',
    'reassembly',
    'transcription',
    'qa',
    'validation'
]

# green means available to proceed
# yellow means in the process of being worked on
# red means stopped or flagged
states = ('green', 'yellow', 'red')


def initialize_state(pk, model, *args, **kwargs):
    """initialize the state of each object upon it's creation"""
    initial_stage = stages[0]
    initial_state = states[0]

    item = model.objects.get(pk=pk)
    item.stage = initial_stage
    item.state = initial_state


def validate_state_object(pk, model, **kwargs):
    """check the schemas for conditions necessary to update the state of the objects"""
    # batch, files, documents
    # file shouldn't contain a rejected document'
    pass


def update_state_object(pk, model, **kwargs):
    """update the state of the object"""
    """state can only move a step ahead or behind"""
    validate_state_object()
    item = model.objects.get(pk=pk)
    current_stage = item.stage
    current_state = item.state
    action = kwargs.get('action')
    if action == 'next':
        next_stage = stages.index(current_stage) + 1
        next_state = states.index(current_state) + 1
    else:
        next_stage = stages.index(current_stage) - 1
        next_state = states.index(current_state) - 1
    item.stage = next_stage
    item.state = next_state
    item.save()


