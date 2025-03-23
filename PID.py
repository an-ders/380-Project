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

    def get_offset(self, hsv, frame_width, color):
        """Takes HSV frame, updates offset"""
        if color == "r":
            range = RED_HSV_RANGE
        elif color == "b":
            range = BLUE_HSV_RANGE
        elif color == "g":
            range = GREEN_HSV_RANGE
        else:
            print("Invalid color.")
            raise

        # Create red mask and keep only bottom 100 pixels
        mask = cv.inRange(
            hsv, range['lower'], range['upper'])
        if color == "r":
            mask[:-100, :] = 0  # Keep only bottom 100 pixels

        # Find red pixels in the bottom region
        pixels = np.where(mask > 0)
            
        if len(pixels[1]) > 0:  # If red line is detected
            # Find max and min X coordinates of the red line
            max_x = np.max(pixels[1])
            min_x = np.min(pixels[1])
            red_center_x = (max_x + min_x) / 2

            # Calculate error (replaces offset)
            center_x = frame_width // 2
            self.error = (red_center_x - center_x)
            print("Offset: ", self.error)
        else:
            # Reset PID variables when line is lost
            self.integral = 0
            self.previous_error = 0
            # If no red line is detected, stop motors
            stop_motors()
            print("No red line detected")

    def calculate_control_signal(self):
        # PID calculations
        self.integral += self.error
        derivative = self.error - self.previous_error
        
        # Calculate control signal
        self.control_signal = (KP * self.error) + (KI * self.integral) + (KD * derivative)
        
        # Clamp control signal to [-1, 1]
        self.control_signal = max(min(self.control_signal, 1), -1)

        # Update previous error
        self.previous_error = self.error

    def get_differential_speed(self):
        # Calculate motor speeds
        if self.control_signal > 0:  # Need to turn right
            left_duty_cycle = MIN_DUTY_CYCLE
            right_duty_cycle = MIN_DUTY_CYCLE * (1 - abs(self.control_signal))
        else: #if self.control_signal < 0:  # Need to turn left
            left_duty_cycle = MIN_DUTY_CYCLE * (1 - abs(self.control_signal))
            right_duty_cycle = MIN_DUTY_CYCLE
        return left_duty_cycle, right_duty_cycle

