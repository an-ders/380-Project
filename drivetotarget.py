import cv2 as cv
import numpy as np
from math import log
from hardware import *
import platform

MAX_TURNS = 9

MIN_LEN = 0.1  # m
MAX_LEN = 0.5 # m
MIN_SPEED = 0.25
MAX_SPEED = 0.55
M = (MAX_SPEED-MIN_SPEED)/(MAX_LEN-MIN_LEN)
B = MAX_SPEED-MAX_LEN*M
REAL_M = 1
REAL_B = 0

def turn():
    pass

def get_real_path_len(line_len):
    path_len = REAL_M*line_len + REAL_B
    return path_len

# TODO TUNE ME - ZARA
def get_optimal_speed(path_len):
    speed = M*path_len + B
    return speed

def drive_to_target_main():
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
    # [*2] Set frame rate
    cap.set(cv.CAP_PROP_FPS, 30)  # Set to 30 frames per second

    total_turns = 0
    while total_turns < MAX_TURNS:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Resize frame for consistency
        frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)
        # frame = cv.resize(frame, (480, 480))

        # Convert to HSV color space
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Create masks for red color
        mask = cv.inRange(
            hsv, RED_HSV_RANGE['lower'], RED_HSV_RANGE['upper'])

        # Apply mask to isolate red regions
        red_regions = cv.bitwise_and(frame, frame, mask=mask)

        # Convert the mask to grayscale for edge detection
        gray = cv.cvtColor(red_regions, cv.COLOR_BGR2GRAY)

        # [*4] Apply Canny edge detection
        edges = cv.Canny(gray, 50, 150)

        # [*5] Use HoughLinesP to detect line segments
        lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

        # Draw the detected lines on the original frame
        points = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]  # Unpack line endpoints
                points.append((x1, y1))
                points.append((x2, y2))
                cv.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw line in green
            highest_point = min(points, key=lambda p: p[1])  # Point with smallest y
            lowest_point = max(points, key=lambda p: p[1])   # Point with largest y
            
            # Draw max and min positions
            frame_width = frame.shape[1]  
            cv.line(frame, (0, highest_point[1]), (frame_width, highest_point[1]), (255, 255, 0), 2)  # Cyan # Draw horizontal line at the highest y-value (topmost detected edge)
            cv.line(frame, (0, lowest_point[1]), (frame_width, lowest_point[1]), (255, 255, 0), 2)  # Cyan # Draw horizontal line at the lowest y-value (bottommost detected edge)

            # PATH LENGTH
            line_len = lowest_point[1] - highest_point[1]
            path_len = get_real_path_len(line_len)
            print(f"Digital Line Length: {line_len:.2f} | Real Line Length: {path_len:.2f}")
            
            # OUTPUTS   
            if path_len < MIN_LEN:
                turn()
                total_turns += 1
            else:
                speed = get_optimal_speed(path_len)
                print(speed)
                #     #offset = get_offset(frame)  # TODO by Anders
                #     #left_speed, right_speed = get_differential_speed(offset, speed)  # TODO by Anders
                drive_motors(speed, speed)
                
        else:
            print("No red line detected")

        # Display the original frame with detected lines
        cv.imshow('Red Line Detection', frame)

        # Break loop on user interrupt (e.g., 'q' key press)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    drive_to_target_main()