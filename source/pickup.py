from .vision import *
from .hardware import *
import cv2 as cv

def pickup(cap):
    
    search_range = 200
    search_speed = 0.1

    # Pickup lego man
    stop_motors()
    sleep(1)
    drive_motors(-search_speed, -search_speed)
    sleep(0.6)
    stop_motors()
    sleep(1)
    drive_motors(-0.1, 0.1)
    
    # Search for the new red line when turning around
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
            if abs(error) < search_range: break

    stop_motors()
    sleep(2)