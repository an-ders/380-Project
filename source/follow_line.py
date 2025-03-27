import cv2 as cv
from .hardware import *
from .vision import *

def follow_line(cap):
    KP = 0.00032 
    KD = 0.00024 

    BASE_SPEED = 0.19
    DEADZONE = 50

    started = False

    error = 0
    derivative = 0
    previous_error = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # Convert to HSV color space
        mask1 = cv.inRange(hsv, RED_HSV_RANGE['lower_red1'], RED_HSV_RANGE['upper_red1'])  # Create masks for red color
        mask2 = cv.inRange(hsv, RED_HSV_RANGE['lower_red2'], RED_HSV_RANGE['upper_red2'])  # Create masks for red color

        mask = cv.bitwise_or(mask1, mask2)  # get all red

        c, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        if (error := getError(c)) is not None:
            started = True
            
            # If error in deadzone dont adjust
            if abs(error) < DEADZONE: continue
            
            # PD control
            derivative = error - previous_error
            
            signal = (KP * error) + (KD * derivative)
            previous_error = error

            # Adjust speed of motors 
            left_speed = BASE_SPEED - signal
            right_speed = BASE_SPEED + signal
            
            print(f"{left_speed:.3f}, {right_speed:.3f}")

            drive_motors(left_speed, right_speed)
        elif started:
            break

    stop_motors()