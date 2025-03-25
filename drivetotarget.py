import cv2 as cv
import numpy as np
from math import log
from hardware import *
import platform
import PID
from collections import deque


MAX_TURNS = 9

MIN_LEN = 0.1  # m
MAX_LEN = 0.5 # m
MIN_DUTY_CYCLE = 0.25
M = (MAX_DUTY_CYCLE-MIN_DUTY_CYCLE)/(MAX_LEN-MIN_LEN)
B = MAX_DUTY_CYCLE-MAX_LEN*M
REAL_M = 1
REAL_B = 0
BUFFER_CAPACITY = 5

def is_target_close(hsv_frame):
    """Takes HSV frame, returns whether blue is close or not"""
    # TODO reactivate
    return False
    blue_mask = cv.inRange(hsv_frame, BLUE_HSV_RANGE['lower'], BLUE_HSV_RANGE['upper'])
    blue_mask[:-100, :] = 0  # Keep only bottom 100 pixels
    blue_pixels = np.where(blue_mask > 0)
    if len(blue_pixels[1]) > 0:
        print("Target Identified.")
        stop_motors()
        return True
    else:
        return False
    
def get_ROI(height, width):
    """
    Creates a binary mask with:
    - The bottom 20% of the frame filled white
    - A triangle above that, connecting the top center to the bottom corners of the 20% line
    - The top 40% of the frame is blacked out (not part of the ROI)

    Returns:
        region_of_interest (np.ndarray): A binary mask (uint8) with ROI marked as 255
    """
    # Create a blank (black) mask
    region_of_interest = np.zeros((height, width), dtype=np.uint8)

    # Bottom 30% starting from 60% height
    roi_start_y = int(height * 0.7)
    roi_end_y = height

    # Middle 50% in X direction
    roi_start_x = int(width * 0.1)
    roi_end_x = int(width * 0.9)

    # Fill only the intersection: vertical 60–100% and horizontal 25–75%
    region_of_interest[roi_start_y:roi_end_y, roi_start_x:roi_end_x] = 255

    return region_of_interest

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
    region_of_interest = get_ROI(native_height, native_width)
    buffer = deque(maxlen=BUFFER_CAPACITY)  # mid_x
    got_line = False  # bool on whether or not line is tracked, prevents premature exit of program
    while not target:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        #frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)  # Resize frame for consistency
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # Convert to HSV color space
        mask1 = cv.inRange(hsv, RED_HSV_RANGE['lower_red1'], RED_HSV_RANGE['upper_red1'])  # Create masks for red color
        mask2 = cv.inRange(hsv, RED_HSV_RANGE['lower_red2'], RED_HSV_RANGE['upper_red2'])  # Create masks for red color

        mask = cv.bitwise_or(mask1, mask2)  # get all red
        mask = cv.bitwise_and(mask, region_of_interest)  # isolate for ROI
        red_regions = cv.bitwise_and(frame, frame, mask=mask)  # Apply mask to isolate red regions

        # # Convert the mask to grayscale for edge detection
        gray = cv.cvtColor(red_regions, cv.COLOR_BGR2GRAY)

        # # [*4] Apply Canny edge detection
        edges = cv.Canny(gray, 50, 150)

        # # [*5] Use HoughLinesP to detect line segments
        lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

        # # Draw the detected lines on the original frame
        points = []
        mask_bgr = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
        if lines is not None:
            got_line = True
            for line in lines:
                x1, y1, x2, y2 = line[0]  # Unpack line endpoints
                points.append((x1, y1))
                points.append((x2, y2))
                cv.line(mask_bgr, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Draw line bounds in red
            highest_point = min(points, key=lambda p: p[0])  # Point with smallest x
            lowest_point = max(points, key=lambda p: p[0])   # Point with largest x
            mid_x = float(lowest_point[0] + (highest_point[0]-lowest_point[0])/2)
            buffer.append(mid_x)

        else:
            buffer.append(0)
            print("No red line detected")
            stop_motors()

        # UPDATE MID_X AND OFFSET regardless of if we detect line or not
        average_mid_x = sum(buffer) / len(buffer)
        if (average_mid_x == 0) and (got_line):
            print("Red line out of sight. Stopping motors.")
            stop_motors()
            break

        offset = (native_width/2) - average_mid_x
        scaled_offset = -1*offset/(native_width/2)

        # Draw vertical line of offset
        cv.line(mask_bgr, (int(average_mid_x), 0), (int(average_mid_x), native_height), (255, 255, 0), 2)  
        pid.calculate_control_signal(scaled_offset)
        left_duty_cycle, right_duty_cycle = pid.get_differential_speed()
        print(left_duty_cycle, right_duty_cycle)
        drive_motors(left_duty_cycle, right_duty_cycle)
        target = is_target_close(hsv)

        # Display the original frame with detected lines
        cv.imshow('Red Line Detection', mask_bgr)

        # Break loop on user interrupt (e.g., 'q' key press)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    drive_to_target_main()