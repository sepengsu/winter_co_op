import numpy as np


def head_position(head_body):
    return abs(head_body.com_pos().z)
def body_position(model):
    return abs(model.com_pos().z)

def head_velocity(head_body):
    return abs(head_body.com_vel().z)

def body_velocity(model):
    return abs(model.com_vel().z)

