"""Module for part 1 of the program. Robot starts following the red line towards the target."""
import cv2 as cv
from hardware import *
import img_processing as imgp
from math import log

MAX_TURNS = 9

# TODO CALIBRATE ME (BELOW)
MIN_LEN = 0.15  # m
MAX_LEN = 1 # m
MIN_SPEED = 0.1
A = 1
B = 0
C = 0
M = 1
Y_INT = 0

red_lower = np.array([0, 100, 100])
red_upper = np.array([10, 255, 255])
red_lower_2 = np.array([160, 100, 100])
red_upper_2 = np.array([180, 255, 255])

# TODO TUNE ME - ZARA
def get_optimal_speed(line_len):
    speed = A*log(line_len + B) + C
    return speed

def get_path_len_from_line(line_len):
    # TODO collect data to calibrate
    path_len = M*line_len + Y_INT
    return path_len

def get_line_len(frame):
    # Resize frame for consistency
    frame = cv.resize(frame, (480, 480))

    # Rotate because our camera is tilted
    frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)

    # Convert to HSV color space
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Create masks for red color
    mask1 = cv.inRange(hsv, red_lower, red_upper)
    mask2 = cv.inRange(hsv, red_lower_2, red_upper_2)
    mask = cv.bitwise_or(mask1, mask2)

    # Apply mask to isolate red regions
    red_regions = cv.bitwise_and(frame, frame, mask=mask)

    # Convert the mask to grayscale for edge detection
    gray = cv.cvtColor(red_regions, cv.COLOR_BGR2GRAY)

    # [*4] Apply Canny edge detection
    edges = cv.Canny(gray, 50, 150)

    # [*5] Use HoughLinesP to detect line segments
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    if lines is not None and len(lines) >= 2:
        first_line = lines[0][0]  # Extract the first detected line
        second_line = lines[1][0]  # Extract the second detected line

    x1_1, y1_1, x2_1, y2_1 = first_line
    x1_2, y1_2, x2_2, y2_2 = second_line

    midpoint_1 = imgp.get_midpoint((x1_1, y1_1), (x1_2, y1_2))  # top points
    midpoint_2 = imgp.get_midpoint((x2_1, y2_1), (x2_2, y2_2))  # bottom points
    line_len = imgp.get_length(midpoint_1, midpoint_2)

    # Draw new center line in green
    cv.line(frame, midpoint_1, midpoint_2, (0, 255, 0), 2)

    # Display the original frame with the drawn line
    cv.imshow('Red Line Detection', frame)
    return line_len

def drive_to_target_main(img):
    # Initialize webcam
    cap = cv.VideoCapture(0)

    # [*1] Set resolution
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)  # Set width to 640 pixels
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)  # Set height to 480 pixels

    # [*2] Set frame rate
    cap.set(cv.CAP_PROP_FPS, 30)  # Set to 30 frames per second

    total_turns = 0
    while True:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        while total_turns < MAX_TURNS:
            line_len = get_line_len(frame)
            if line_len < MIN_LEN:
                # TODO 90 degree turn program
                total_turns += 1
            else:
                speed = get_optimal_speed(line_len)
                #offset = get_offset(img)  # TODO by Anders
                #left_speed, right_speed = get_differential_speed(offset, speed)  # TODO by Anders
                drive_motors(speed, speed)
        # go to part 2