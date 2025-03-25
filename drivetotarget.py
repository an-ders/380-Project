import cv2 as cv
import numpy as np
from math import log
from hardware import *
import platform
import PID

MAX_TURNS = 9

MIN_LEN = 0.1  # m
MAX_LEN = 0.5 # m
MIN_DUTY_CYCLE = 0.25
M = (MAX_DUTY_CYCLE-MIN_DUTY_CYCLE)/(MAX_LEN-MIN_LEN)
B = MAX_DUTY_CYCLE-MAX_LEN*M
REAL_M = 1
REAL_B = 0

def get_real_path_len(line_len):
    path_len = REAL_M*line_len + REAL_B
    return path_len

def get_optimal_speed(path_len):
    speed = M*path_len + B
    return speed

def is_target_close(hsv_frame):
    """Takes HSV frame, returns whether blue is close or not"""
    blue_mask = cv.inRange(hsv_frame, BLUE_HSV_RANGE['lower'], BLUE_HSV_RANGE['upper'])
    blue_mask[:-100, :] = 0  # Keep only bottom 100 pixels
    blue_pixels = np.where(blue_mask > 0)
    if len(blue_pixels[1]) > 0:
        print("Target Identified.")
        stop_motors()
        return True
    else:
        return False

def drive_to_target_main():
    # Initialize webcam
    if platform.system() == 'Windows':
        cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    else:
        cap = cv.VideoCapture(0)

    native_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    native_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    
    pid = PID.PID()
    target = False
    while not target:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        #frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)  # Resize frame for consistency
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # Convert to HSV color space
        mask = cv.inRange(hsv, RED_HSV_RANGE['lower'], RED_HSV_RANGE['upper'])  # Create masks for red color
        red_regions = cv.bitwise_and(frame, frame, mask=mask)  # Apply mask to isolate red regions

        # # Convert the mask to grayscale for edge detection
        gray = cv.cvtColor(red_regions, cv.COLOR_BGR2GRAY)

        # # [*4] Apply Canny edge detection
        edges = cv.Canny(gray, 50, 150)

        # # [*5] Use HoughLinesP to detect line segments
        lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

        # # Draw the detected lines on the original frame
        points = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]  # Unpack line endpoints
                points.append((x1, y1))
                points.append((x2, y2))
                cv.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw line in green
            highest_point = min(points, key=lambda p: p[0])  # Point with smallest x
            lowest_point = max(points, key=lambda p: p[0])   # Point with largest x
            mid_x = float(lowest_point[0] + (highest_point[0]-lowest_point[0])/2)
            offset = (native_width/2) - mid_x
            scaled_offset = -1*offset/(native_width/2)
            
            # Draw max and min positions
            frame_height = frame.shape[0] 
            cv.line(frame, (int(mid_x), 0), (int(mid_x), frame_height), (255, 255, 0), 2)  # Cyan # Draw vertical line at the highest y-value (topmost detected edge)
            # cv.line(frame, (highest_point[0], 0), (highest_point[0], frame_height), (255, 255, 0), 2)  # Cyan # Draw vertical line at the highest y-value (topmost detected edge)
            # cv.line(frame, (lowest_point[0], 0), (lowest_point[0], frame_height), (255, 255, 0), 2)  # Cyan # Draw vertical line at the lowest y-value (bottommost detected edge)

        #     # PATH LENGTH
        #     line_len = lowest_point[1] - highest_point[1]
        #     path_len = get_real_path_len(line_len)
        #     print(f"Digital Line Length: {line_len:.2f} | Real Line Length: {path_len:.2f}")
            
            # OUTPUTS
            #optimal_duty_cycle = get_optimal_speed(path_len) # TODO implement speed control
            #pid.get_offset(hsv, native_width, "r")
            pid.calculate_control_signal(scaled_offset)
            left_duty_cycle, right_duty_cycle = pid.get_differential_speed()
            print(left_duty_cycle, right_duty_cycle)
            drive_motors(left_duty_cycle, right_duty_cycle)

        else:
            print("No red line detected")
            stop_motors()

        target = is_target_close(hsv)

        # Display the original frame with detected lines
        cv.imshow('Red Line Detection', mask)

        # Break loop on user interrupt (e.g., 'q' key press)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    drive_to_target_main()