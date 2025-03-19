"""Module for part 1 of the program. Robot starts following the red line towards the target."""
import cv2 as cv
# from hardware import *
import img_processing as imgp
from math import log
import numpy as np

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

# TODO TUNE ME - ZARA
def get_optimal_speed(line_len):
    speed = A*log(line_len + B) + C
    return speed

def get_path_len_from_line(line_len):
    # TODO collect data to calibrate
    path_len = M*line_len + Y_INT
    return path_len

def drive_to_target_main():
    # Initialize webcam
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)

    # [*1] Set resolution
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)  # Set width to 640 pixels
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)  # Set height to 480 pixels

    # [*2] Set frame rate
    cap.set(cv.CAP_PROP_FPS, 30)  # Set to 30 frames per second

    # [*3] Define HSV range for red color
    red_lower = np.array([0, 100, 100])
    red_upper = np.array([10, 255, 255])
    red_lower_2 = np.array([160, 100, 100])
    red_upper_2 = np.array([180, 255, 255])

    total_turns = 0
    while True:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        while total_turns < MAX_TURNS:
            frame = cv.resize(frame, (480, 480))  # Resize frame for consistency
            # frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)  # Rotate because our camera is tilted
            # TODO rotate
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # Convert to HSV color space

            # Create masks for red color
            mask1 = cv.inRange(hsv, red_lower, red_upper)
            mask2 = cv.inRange(hsv, red_lower_2, red_upper_2)
            mask = cv.bitwise_or(mask1, mask2)

            # Apply mask to isolate red regions
            red_regions = cv.bitwise_and(frame, frame, mask=mask) # Apply mask to isolate red regions
            gray = cv.cvtColor(red_regions, cv.COLOR_BGR2GRAY)  # Convert the mask to grayscale for edge detection
            cv.imshow('Red Line Detection', gray)

            # [*4] Apply Canny edge detection
            edges = cv.Canny(gray, 50, 150)
            # [*5] Use HoughLinesP to detect line segments
            lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

            if lines is not None:
                print("Red line detected")
                # Extract (x, y) pairs
                points = []
                for line in lines:
                    x1, y1, x2, y2 = line[0]  # Unpack correctly
                    points.append((x1, y1))
                    points.append((x2, y2))
                # Find the highest and lowest y-value points
                highest_point = min(points, key=lambda p: p[1])  # Point with smallest y
                lowest_point = max(points, key=lambda p: p[1])   # Point with largest y

                # Draw a line between these two points
                cv.line(frame, highest_point, lowest_point, (0, 255, 0), 2)
                highest_y = min(highest_point[1])  # Find the smallest y-value
                lowest_y = max(lowest_point[1])
            
                line_len = lowest_y - highest_y
                print(line_len)
                cv.line(frame, highest_point, lowest_point, (0, 255, 0), 2)
                # Display the original frame with the drawn line
                cv.imshow('Red Line Detection', frame)
                # if line_len < MIN_LEN:
                #     # TODO 90 degree turn program
                #     total_turns += 1
                # else:
                #     speed = get_optimal_speed(line_len)
                #     #offset = get_offset(img)  # TODO by Anders
                #     #left_speed, right_speed = get_differential_speed(offset, speed)  # TODO by Anders
                #     drive_motors(speed, speed)
                print(line_len)
            else:
                print("No red line detected.")
        cv.imshow('Red Line Detection', frame)

        # Break loop on user interrupt (e.g., 'q' key press)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    drive_to_target_main()