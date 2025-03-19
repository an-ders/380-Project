import cv2 as cv
import numpy as np
import time as timer
from constants import *
from hardware import *

MAX_SPEED = 0.6


def main():
    # Initialize webcam
    cap = cv.VideoCapture(0)

    # Get native resolution and swap width/height for portrait orientation
    native_width = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))  # Swapped
    native_height = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))  # Swapped

    # Set video parameters
    # Original height becomes width
    cap.set(cv.CAP_PROP_FRAME_WIDTH, native_height)
    # Original width becomes height
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, native_width)

    print("Starting line following. Press 'q' to quit.")

    while True:
        start_time = timer.time()  # Start of frame processing

        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Rotate frame 90 degrees clockwise immediately after capture
        frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)

        # Convert to HSV color space for processing
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Create red mask and keep only bottom 100 pixels
        red_mask = cv.inRange(
            hsv, RED_HSV_RANGE['lower'], RED_HSV_RANGE['upper'])
        red_mask[:-100, :] = 0  # Keep only bottom 100 pixels

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

            x_low = np.max(asd[1])
            x_high = np.min(asd[1])

            # Calculate offset from center (-1 to 1)
            center_x = native_width // 2
            offset = (red_center_x - center_x) / center_x

            # Apply exponential scaling to the offset
            k = 0.25  # Adjust this value to change sensitivity
            exp_offset = np.sign(offset) * (np.exp(k * abs(offset)) - 1)

            # Calculate motor speeds (0 to 1)
            base_speed = 0.4  # Base speed for forward motion
            if offset > 0:  # Red line is to the right
                left_speed = base_speed 
                right_speed = base_speed * (1 - abs(exp_offset))
            else:  # Red line is to the left
                left_speed = base_speed * (1 - abs(exp_offset))
                right_speed = base_speed 

            # Set motor speeds
            if x_low <= 1:
                print("turn left")
            elif x_high >= 718:
                print("turn right")
            else:
                print("straight")
                #drive_motors(left_speed, right_speed)

            # # Draw debug visualization
            cv.circle(frame, (int(red_center_x), native_height - 50),
                      5, (0, 0, 255), -1)
            cv.line(frame, (min_x, native_height - 100), (max_x,
                    native_height - 100), (0, 255, 0), 2)  # Line showing red range
            cv.line(frame, (center_x, native_height - 100),
                    (center_x, native_height), (255, 0, 0), 2)  # Center line

            # Print debug info
            print(f"X Range: {min_x} to {max_x}, Center X: {red_center_x:.1f}")
            print(f"Offset: {offset:.2f}, Exp Offset: {exp_offset:.2f}")
            print(
                f"Motor speeds - Left: {left_speed:.2f}, Right: {right_speed:.2f}")
        else:
            # If no red line is detected, stop motors
            #stop_motors()
            print("No red line detected")

        # Display the frame (already in portrait orientation)
        cv.imshow('Line Following', frame)

        # Calculate how long to wait to maintain FPS
        process_time = timer.time() - start_time
        print(f"Process time: {process_time:.4f}s")
        wait_time = max(1.0/FPS - process_time, 0)
        print(f"Wait time: {wait_time:.4f}s")

        # Break loop if 'q' is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            print("Stopping line following")
            break

    # Cleanup
    stop_motors()
    cap.release()
    cv.destroyAllWindows()


main()
