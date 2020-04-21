from app.models import *
""" this module manages the document workflow and states of individual objects """
""":key primary key"""
""":keyword batch"""
""":keyword file"""
""":keyword document"""


def initialize_state(pk, *args, **kwargs):
    """initialize the state of each object upon it's creation"""
    pass


def validate_state_object(**kwargs):
    """check the schemas for conditions necessary to update the state of the objects"""
    pass

def update_state_object(**kwargs):
    """update the state of the object"""
    """state can only move a step ahead or behind"""
    validate = validate_state_object()
    pass