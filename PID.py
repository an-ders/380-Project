import cv2 as cv
from hardware import *

"""
Use a systematic approach like Ziegler-Nichols Method or manual tuning:

Manual Tuning Approach
    
Set Ki and Kd to Zero. Start with only Kp and gradually increase it until the robot follows the line but oscillates.
Increase Kd. Add small values of Kd to dampen oscillations and smooth movement.
Add Ki. If the robot has slow corrections or drifts over time, increase Ki slightly to improve steady-state accuracy.
"""

KP = 0.01  # Proportional gain
KI = 0.0  # Integral gain
KD = 0.0  # Derivative gain

class PID:
    def __init__(self):
        self.previous_error = 0
        self.integral = 0
        self.error = 0
        # derivative does not need to be a class variable

    def calculate_control_signal(self, offset):
        # PID calculations
        self.error = offset
        self.integral += self.error
        derivative = self.error - self.previous_error
        
        # Calculate control signal
        self.control_signal = (KP * self.error) + (KI * self.integral) + (KD * derivative)
        
        # Clamp control signal to [-1, 1]
        # self.control_signal = max(min(self.control_signal, 1), -1)

        # Update previous error
        self.previous_error = self.error

    def get_differential_speed(self):
        # Calculate motor speeds
        left_duty_cycle = MIN_DUTY_CYCLE + self.control_signal
        right_duty_cycle = MIN_DUTY_CYCLE - self.control_signal
        # if self.control_signal > 0:  # Need to turn right
        #     left_duty_cycle = MIN_DUTY_CYCLE
        #     right_duty_cycle = MIN_DUTY_CYCLE * (1 - abs(self.control_signal))
        # else: #if self.control_signal < 0:  # Need to turn left
        #     left_duty_cycle = MIN_DUTY_CYCLE * (1 - abs(self.control_signal))
        #     right_duty_cycle = MIN_DUTY_CYCLE
        return left_duty_cycle, right_duty_cycle

