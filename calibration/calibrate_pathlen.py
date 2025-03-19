""" INSTRUCTIONS
Let the camera observe the path. Hit r to record a data point. The digital line length will be recorded. 
The user must measure the corresponding physical path. The program waits for user input to enter this distance 
in meters. After 20 data points, the program will output an Excel sheet that can be used for calibration."""

import cv2 as cv
import numpy as np
import pandas as pd

NUM_TESTS = 20

def calibrate_pathlen_main():
    # Initialize webcam
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)

    # [*1] Set resolution
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

    # [*3] Define HSV range for red color
    red_lower = np.array([0, 100, 100])
    red_upper = np.array([10, 255, 255])
    red_lower_2 = np.array([160, 100, 100])
    red_upper_2 = np.array([180, 255, 255])
    num_points = 0

    digital_lens = []
    real_lens = []
    while num_points < NUM_TESTS:
        line_len = 0
        while not cv.waitKey(1) & 0xFF == ord('r'):
            # Capture frame
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            # Resize frame for consistency
            #frame = cv.resize(frame, (480, 480))
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

            # Display the original frame with detected lines
            cv.imshow('Red Line Detection', frame)
        # RECORD LINE LEN AND WAIT FOR USER INPUT
        print(f"Digital Line Length: {line_len:.2f}")
        measured_distance = float(input("Enter measured distance: "))
        digital_lens.append(line_len)
        real_lens.append(measured_distance)
        num_points += 1

    cap.release()
    cv.destroyAllWindows()

    df = pd.DataFrame({
        "Digital Length": digital_lens,
        "Real Length": real_lens
    })

    # Save to an Excel file
    df.to_excel("Path Length Calibration.xlsx", index=False)

if __name__ == "__main__":
    calibrate_pathlen_main()