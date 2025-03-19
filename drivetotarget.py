import cv2 as cv
import numpy as np
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

def get_real_path_len(line_len):
    # TODO collect data to calibrate
    path_len = M*line_len + Y_INT
    return path_len

# TODO TUNE ME - ZARA
def get_optimal_speed(line_len):
    speed = A*log(line_len + B) + C
    return speed

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
    while total_turns < MAX_TURNS:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Resize frame for consistency
        frame = cv.resize(frame, (480, 480))

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
            print(line_len)
            path_len = get_real_path_len(line_len)
            print(f"Digital Line Length: {line_len:.2f} | Real Line Length: {path_len:.2f}")
            
            # OUTPUTS   
            # if line_len < MIN_LEN:
                #     # TODO 90 degree turn program
                #     total_turns += 1
                # else:
                #     speed = get_optimal_speed(line_len)
                #     #offset = get_offset(img)  # TODO by Anders
                #     #left_speed, right_speed = get_differential_speed(offset, speed)  # TODO by Anders
                #     drive_motors(speed, speed)
                
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