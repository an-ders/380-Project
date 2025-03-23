import cv2 as cv
from hardware import *

KP = 0.8  # Proportional gain
KI = 0.01  # Integral gain
KD = 0.1  # Derivative gain

class PID:
    def __init__(self):
        self.previous_error = 0
        self.integral = 0

    def get_offset(frame, frame_width):
        # Convert to HSV color space for processing
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Create red mask and keep only bottom 100 pixels
        red_mask = cv.inRange(
            hsv, RED_HSV_RANGE['lower'], RED_HSV_RANGE['upper'])
        red_mask[:-100, :] = 0  # Keep only bottom 100 pixels

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        test = cv.inRange(
            hsv, RED_HSV_RANGE['lower'], RED_HSV_RANGE['upper'])
        test[:-400, :] = 0  # Keep only bottom 100 pixels

        # Find red pixels in the bottom region
        red_pixels = np.where(red_mask > 0)
        asd = np.where(test > 0)
            
        if len(red_pixels[1]) > 0:  # If red line is detected
            # Find max and min X coordinates of the red line
            max_x = np.max(red_pixels[1])
            min_x = np.min(red_pixels[1])
            red_center_x = (max_x + min_x) / 2

            # Calculate error (replaces offset)
            center_x = native_width // 2
            error = (red_center_x - center_x)
