import cv2 as cv
import numpy as np
import time as timer
from hardware import *
import platform

MAX_DUTY_CYCLE = 0.6

# Add PID constants at the top with other constants
KP = 0.8  # Proportional gain
KI = 0.01  # Integral gain
KD = 0.1  # Derivative gain

def line_follow_main():
    # Initialize webcam
    if platform.system() == 'Windows':
        cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    else:
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

    # Add PID variables
    previous_error = 0
    integral = 0

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

            # PID calculations
            integral += error
            derivative = error - previous_error
            
            # Calculate control signal
            control_signal = (KP * error) + (KI * integral) + (KD * derivative)
            
            # Clamp control signal to [-1, 1]
            control_signal = max(min(control_signal, 1), -1)

            # Calculate motor speeds
            base_speed = 0.25
            if control_signal > 0:  # Need to turn right
                left_speed = base_speed
                right_speed = base_speed * (1 - abs(control_signal))
            else:  # Need to turn left
                left_speed = base_speed * (1 - abs(control_signal))
                right_speed = base_speed

            # Update previous error
            previous_error = error

            # Debug info
            print(f"Error: {error:.2f}, Control: {control_signal:.2f}")
            print(f"Motor speeds - Left: {left_speed:.2f}, Right: {right_speed:.2f}")

            # Set motor speeds
            
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
        else:
            # Reset PID variables when line is lost
            integral = 0
            previous_error = 0
            # If no red line is detected, stop motors
            #stop_motors()
            print("No red line detected")

        # Display the frame (already in portrait orientation)
        cv.imshow('Line Following', frame)

        # Break loop if 'q' is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            print("Stopping line following")
            break

    # Cleanup
    # stop_motors()
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    line_follow_main()