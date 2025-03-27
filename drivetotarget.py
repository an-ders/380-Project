import cv2 as cv
import numpy as np
from math import log
from hardware import *
import platform
import PID
from collections import deque
import matplotlib.pyplot as plt

STARTUP_FRAMES = 15  # number of frames to throw away on startup
SECTION_OF_FRAME = 0.8  # bottom percentage of frame to declare as regiion of interest
VERBOSE = False
DELAY = 1
MAX_TURNS = 9

MIN_LEN = 0.1  # m
MAX_LEN = 0.5 # m
M = (MAX_DUTY_CYCLE-MIN_DUTY_CYCLE)/(MAX_LEN-MIN_LEN)
B = MAX_DUTY_CYCLE-MAX_LEN*M
REAL_M = 1
REAL_B = 0
BUFFER_CAPACITY = 5

KP = 0.15  # Proportional gain
KI = 0.0  # Integral gain
KD = 0.0  # Derivative gain

base_speed = 0.1
accel = 0.005

error = 0
integral = 0
derivative = 0
previous_error = 0

def drive_to_target_main():
    # Initialize webcam
    if platform.system() == 'Windows':
        cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    else:
        cap = cv.VideoCapture(0)

    native_height = 340
    native_width = 260
    
    pid = PID.PID()
    target = False
    got_line = False  # bool on whether or not line is tracked, prevents premature exit of program
    count = STARTUP_FRAMES
    while not target:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # Convert to HSV color space
        mask1 = cv.inRange(hsv, RED_HSV_RANGE['lower_red1'], RED_HSV_RANGE['upper_red1'])  # Create masks for red color
        mask2 = cv.inRange(hsv, RED_HSV_RANGE['lower_red2'], RED_HSV_RANGE['upper_red2'])  # Create masks for red color

        mask = cv.bitwise_or(mask1, mask2)  # get all red

        c, h = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        if c:
            temp = max(c, key=cv.contourArea)
            mom = cv.moments(temp)

            if mom["m00"]:
                x = int(mom["m10"] / mom["m00"])
                y = int(mom["m01"] / mom["m00"])

            # if base_speed < base_speed_max:
            #     base_speed = base_speed + accel
            
            # if base_speed > base_speed_max:
            #     base_speed = base_speed_max

            error = (native_width // 2) - x
            integral += error
            derivative = error - previous_error

            if error < 10:
                continue
            
            # Calculate control signal
            signal = (KP * error) + (KI * integral) + (KD * derivative)

            # Update previous error
            previous_error = error

            left_speed = base_speed + signal
            right_speed = base_speed - signal
            print(x, y)
            # print(f"{left_speed:.3f}, {right_speed:.3f}")

        else:
            print("No red line detected")
            stop_motors()

        # Display the original frame with detected lines    

        # Break loop on user interrupt (e.g., 'q' key press)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    drive_to_target_main()