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



def validate_state_object(**kwargs):
    """check the schemas for conditions necessary to update the state of the objects"""
    # batch, files, documents
    pass


def update_state_object(**kwargs):
    """update the state of the object"""
    """state can only move a step ahead or behind"""
    validate = validate_state_object()
    pass
