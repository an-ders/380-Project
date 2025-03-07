import cv2 as cv
import numpy as np
import time
from constants import *
from hardware import *

MAX_SPEED = 0.6

def main():
    # Initialize webcam
    cap = cv.VideoCapture(0)
    
    # Get native resolution
    native_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    native_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    
    # Set video parameters
    cap.set(cv.CAP_PROP_FRAME_WIDTH, native_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, native_height)
    
    print("Starting line following. Press 'q' to quit.")
    
    while True:
        start_time = time.time()  # Start of frame processing

        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Convert to HSV color space for processing
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Create red mask and keep only rightmost 100 pixels
        red_mask = cv.inRange(hsv, RED_HSV_RANGE['lower'], RED_HSV_RANGE['upper'])
        red_mask[:, :-100] = 0  # Keep only rightmost 100 pixels

        # Find red pixels in the right region
        red_pixels = np.where(red_mask > 0)

        if len(red_pixels[0]) > 0:  # If red line is detected
            # Find max and min Y coordinates of the red line
            max_y = np.max(red_pixels[0])
            min_y = np.min(red_pixels[0])
            red_center_y = (max_y + min_y) / 2
            
            # Calculate offset from center (-1 to 1)
            center_y = native_height // 2
            offset = (red_center_y - center_y) / center_y
            
            # Apply exponential scaling to the offset
            k = 2.0  # Adjust this value to change sensitivity
            exp_offset = np.sign(offset) * (np.exp(k * abs(offset)) - 1)
            
            # Calculate motor speeds (0 to 1)
            base_speed = 0.5  # Base speed for forward motion
            if offset > 0:  # Red line is below center
                left_speed = base_speed * (1 + exp_offset)
                right_speed = base_speed * (1 - exp_offset)
            else:  # Red line is above center
                left_speed = base_speed * (1 - abs(exp_offset))
                right_speed = base_speed * (1 + abs(exp_offset))

            # Ensure speeds stay within bounds (0 to 1)
            left_speed = np.clip(left_speed, 0, 1)
            right_speed = np.clip(right_speed, 0, 1)

            # Set motor speeds
            drive_motors(left_speed * MAX_SPEED, right_speed * MAX_SPEED)

            # Draw debug visualization
            cv.circle(frame, (native_width - 50, int(red_center_y)), 5, (0, 0, 255), -1)
            cv.line(frame, (native_width - 100, min_y), (native_width - 100, max_y), (0, 255, 0), 2)  # Line showing red range
            cv.line(frame, (native_width - 100, center_y), (native_width, center_y), (255, 0, 0), 2)  # Center line
            
            # Print debug info
            print(f"Y Range: {min_y} to {max_y}, Center Y: {red_center_y:.1f}")
            print(f"Offset: {offset:.2f}, Exp Offset: {exp_offset:.2f}")
            print(f"Motor speeds - Left: {left_speed:.2f}, Right: {right_speed:.2f}")
        else:
            # If no red line is detected, stop motors
            stop_motors()
            print("No red line detected")

        # Display the frame
        display_frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
        cv.imshow('Line Following', display_frame)

        # Calculate how long to wait to maintain FPS
        process_time = time.time() - start_time
        wait_time = max(1.0/FPS - process_time, 0)
        time.sleep(wait_time)

        # Break loop if 'q' is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            print("Stopping line following")
            break

    # Cleanup
    stop_motors()
    cap.release()
    cv.destroyAllWindows()

main()




