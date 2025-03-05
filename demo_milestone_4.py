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

    # Phase 1: Wait for red line detection
    print("Phase 1: Waiting for red line")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Convert to HSV and create red mask
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        red_mask = cv.inRange(hsv, RED_HSV_RANGE['lower'], RED_HSV_RANGE['upper'])
        
        # Check if red is detected
        if np.any(red_mask > 0):
            print("Red detected! Starting movement sequence...")
            break

        time.sleep(1/FPS)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Phase 2: Drive forward for 3 seconds
    print("Phase 2: Driving forward")
    start_time = time.time()
    drive_forward()
    while time.time() - start_time < 3:
        time.sleep(1/FPS)

    # Phase 3: Stop and turn
    print("Phase 3: Turning")
    stop()
    turn()

    # Phase 4: Drive backward
    print("Phase 4: Driving backward")
    drive_backward()
    time.sleep(3)  # Drive backward for 3 seconds
    stop()

    # Cleanup
    cap.release()
    cv.destroyAllWindows()

demo()
