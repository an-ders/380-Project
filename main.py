import cv2 as cv
import numpy as np
import time
from constants import *

# init video code




def main():
    # Initialize webcam
    cap = cv.VideoCapture(0)

    # Set video parameters
    native_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    native_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    # Set video parameters
    cap.set(cv.CAP_PROP_FRAME_WIDTH, native_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, native_height)
    cap.set(cv.CAP_PROP_FPS, FPS)

    # Swap width and height since we're rotating 90 degrees
    temp = native_width
    native_width = native_height
    native_height = temp

    # Define HSV ranges for colors
    # Red has two ranges due to how it wraps around in HSV

    while True:
        # Add a delay to control frame rate (e.g., 10 FPS)
        time.sleep(1/FPS)

        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Resize frame for consistency
        frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
        frame = cv.resize(frame, (native_width, native_height))

        # Convert to HSV color space
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) 

        # red_mask = cv.bitwise_or(red_mask1, red_mask2)
        red_mask = cv.inRange(
            hsv, RED_HSV_RANGE['lower'], RED_HSV_RANGE['upper'])
        green_mask = cv.inRange(
            hsv, GREEN_HSV_RANGE['lower'], GREEN_HSV_RANGE['upper'])
        blue_mask = cv.inRange(
            hsv, BLUE_HSV_RANGE['lower'], BLUE_HSV_RANGE['upper'])
        
        # Mask off all but bottom 100 pixels for red mask
        red_mask[:FRAME_HEIGHT - 100, :] = 0

        # Draw horizontal line showing bottom 100 pixel region
        cv.line(frame, (0, native_height - 100), 
                (native_width, native_height - 100), (0, 0, 255), 2)

        # Find red pixels in bottom region
        red_pixels = np.where(red_mask > 0)

        if len(red_pixels[1]) > 0:  # If any red pixels are found
            # Get leftmost (min x) and rightmost (max x) red points
            red_left_x = np.min(red_pixels[1])
            red_right_x = np.max(red_pixels[1])

            # Draw vertical red lines at min and max x values
            cv.line(frame, (red_left_x, 0), (red_left_x, 
                    frame.shape[0]), (0, 0, 255), 2)  # Left line in red
            cv.line(frame, (red_right_x, 0), (red_right_x,
                    frame.shape[0]), (0, 0, 255), 2)  # Right line in red

        # Apply mask to isolate green regions

        # -------------------------  GREEN ---------------------------------------------------

        cv.imshow('Red Line Detection', frame)

        # Break loop on user interrupt (e.g., 'q' key press)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


# Run the function
main()
