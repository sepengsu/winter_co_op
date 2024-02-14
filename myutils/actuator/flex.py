import numpy as np
import time
import yaml
import re

def angleformula(A, B = np.array([0, 1, 0])):
    dot_product = np.dot(A, B)
    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)
    cos_theta = dot_product / (norm_A * norm_B)
    theta = np.arccos(cos_theta)
    return np.degrees(theta)

# Define the proportional-derivative control function for trunk balance
def trunk_balance_control(theta, theta_ref, kp, kd, theta_dot):
    """
    Calculate the stimulation signal for trunk balance control based on a proportional-derivative (PD) controller.

    Parameters:
    theta (float): The current forward lean angle of the trunk with respect to gravity.
    theta_ref (float): The reference lean angle of the trunk.
    kp (float): The proportional gain.
    kd (float): The derivative gain.
    theta_dot (float): The derivative of the trunk's forward lean angle (i.e., the rate of change of theta).

    Returns:
    float: The stimulation signal for the gluteus muscle group (GLU) and the hip flexor muscle group (HFL).
    """
    return kp * (theta - theta_ref) + kd * theta_dot

class BodyOrientationReflex:
    def __init__(self, source, target, axis=[0, 0, 1], P0=0, KP=0, allow_neg_P=True, V0=0, KV=0, allow_neg_V=True, C0=0, min_control_value=float('-inf'), max_control_value=float('inf'), delay=0):
        super().__init__()
        self.source = source
        self.target = target
        self.axis = axis
        self.P0 = P0
        self.allow_neg_P = allow_neg_P
        self.V0 = V0
        self.KV = KV
        self.allow_neg_V = allow_neg_V
        self.C0 = C0
        self.min_control_value = min_control_value
        self.max_control_value = max_control_value
        self.delay = delay
        self.KP = KP

    def calculate_reflex(self, current_orientation, current_velocity):
        # Assuming current_orientation and current_velocity are given or can be calculated
        orientation_error = self.P0 - current_orientation
        velocity_error = self.V0 - current_velocity

        # Apply the orientation and velocity feedback gains
        orientation_control = self.KP * orientation_error
        velocity_control = self.KV * velocity_error

        # Calculate the final control value
        control_value = orientation_control + velocity_control + self.C0

        # Apply the min and max control value limits
        control_value = max(self.min_control_value, min(control_value, self.max_control_value))

        # Apply the delay if necessary
        # This would require a more complex implementation to simulate real-time delay effects

        return control_value
  
def _control(torso):
    with open(r'C:\Users\PC\Desktop\SJW\dep\myutils\actuator\reflex_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    bending = BodyOrientationReflex(**config['lumbar_bending'])
    rotation = BodyOrientationReflex(**config['lumbar_rotation'])
    extension = BodyOrientationReflex(**config['lumbar_extension'])
    output = np.array([0,0,0])
    output[0] = bending.calculate_reflex(torso.orientation().x,torso.ang_vel().x)
    output[1] = rotation.calculate_reflex(torso.orientation().y,torso.ang_vel().y)
    output[2] = extension.calculate_reflex(torso.orientation().z,torso.ang_vel().z)
    print(sum(output)==0)
    return output


class PDController:
    def __init__(self, kp, kd, theta_ref, min_output=float('-inf'), max_output=float('inf')):
        self.kp = kp
        self.kd = kd
        self.theta_ref = theta_ref
        self.min_output = min_output
        self.max_output = max_output

    def calculate_control(self, current_theta, current_theta_dot):
        # Calculate the error between current and desired orientation
        error = self.theta_ref - current_theta

        # Calculate the derivative term
        derivative = current_theta_dot

        # PD Control
        control_signal = self.kp * error + self.kd * derivative

        # Apply the output limits
        control_signal = max(self.min_output, min(control_signal, self.max_output))
        return control_signal


COEF = {
    'bending':{'kp':1.91*20,'kd': 0.25*20,'theta_ref': 0},
    'rotation':{'kp':1.91*20,'kd': 0.25*20,'theta_ref': 0},
    'extension':{'kp':1.91*20,'kd': 0.25*20,'theta_ref': 0},
}
with open(r'C:\Users\PC\Desktop\SJW\dep\myutils\actuator\reflex_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# COEF = {
#     'bending':{'kp':config['lumbar_bending']['KP'],'kd': config['lumbar_bending']['KV'],'theta_ref': config['lumbar_bending']['target']},
#     'rotation':{'kp':config['lumbar_rotation']['KP'],'kd': config['lumbar_rotation']['KV'],'theta_ref': config['lumbar_rotation']['target']},
#     'extension':{'kp':config['lumbar_extension']['KP'],'kd': config['lumbar_extension']['KV'],'theta_ref': config['lumbar_extension']['target']},
# }


def pdcontrol(torso):
    bending = PDController(**COEF['bending'])
    rotation = PDController(**COEF['rotation'])
    extension = PDController(**COEF['extension'])

    output = np.array([0,0,0],dtype=np.float64)
    output[0] = bending.calculate_control(torso.orientation().x,torso.ang_vel().x)
    output[1] = rotation.calculate_control(torso.orientation().y,torso.ang_vel().y)
    output[2] = extension.calculate_control(torso.orientation().z,torso.ang_vel().z)
    # print(output)
    return output
