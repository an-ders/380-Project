import cv2 as cv
import numpy as np
import time
from constants import *
from hardware import *


def demo():
    # Initialize webcam
    cap = cv.VideoCapture(0)

    # Set video parameters
    native_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    native_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    # Set video parameters
    cap.set(cv.CAP_PROP_FRAME_WIDTH, native_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, native_height)
    cap.set(cv.CAP_PROP_FPS, FPS)

    # Phase 1: Drive forward for 3 seconds
    print("Phase 1: Driving forward")
    start_time = time.time()
    drive_forward()
    while time.time() - start_time < 3:
        time.sleep(1/FPS)  # Small delay to prevent CPU overload
    
    # Phase 2: Drive backward for 3 seconds
    print("Phase 2: Driving backward")
    start_time = time.time()
    drive_backward()
    while time.time() - start_time < 3:
        time.sleep(1/FPS)

    # Phase 3: Drive forward until red is detected
    print("Phase 3: Driving forward until red detection")
    while True:
        drive_forward()
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Convert to HSV and create red mask
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        red_mask = cv.inRange(hsv, RED_HSV_RANGE['lower'], RED_HSV_RANGE['upper'])
        
        # Check if red is detected (if there are any white pixels in the mask)
        if np.any(red_mask > 0):
            print("Red detected! Stopping and turning...")
            stop()  # Stop before turning
            turn()  # Call the turn function
            break

        # Add a small delay to control frame rate
        time.sleep(1/FPS)

        # Allow manual interrupt
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    stop()
    cap.release()
    cv.destroyAllWindows()

demo()
