import cv2 as cv
import numpy as np
import time

wheel_diameter = 1
wheel_distance = 1

current_direction = 1

turn_radius = 1

def adjust_left_wheel(speed):
        return speed

def adjust_right_wheel(speed):
    return speed

def drive(left, right):
    return

def detect_red_line():
    # Initialize webcam
    cap = cv.VideoCapture(0)

    # [*1] Set resolution
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)  # Set width to 640 pixels
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)  # Set height to 480 pixels

    # [*2] Set frame rate
    cap.set(cv.CAP_PROP_FPS, 10)  # Set to 30 frames per second

    # [*3] Define HSV range for red color
    red_lower = np.array([0, 100, 100])
    red_upper = np.array([10, 255, 255])
    red_lower_2 = np.array([160, 100, 100])
    red_upper_2 = np.array([180, 255, 255])

    # Define HSV range for green color
    green_lower = np.array([40, 100, 100])
    green_upper = np.array([80, 255, 255])

    while True:
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

        # Create masks for green color
        green_mask = cv.inRange(hsv, green_lower, green_upper)

        # Apply mask to isolate green regions
        green_regions = cv.bitwise_and(frame, frame, mask=green_mask)

        # Convert the mask to grayscale for edge detection
        gray = cv.cvtColor(red_regions, cv.COLOR_BGR2GRAY)

        # [*4] Apply Canny edge detection
        edges = cv.Canny(gray, 50, 150)

        # [*5] Use HoughLinesP to detect line segments
        lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

        # Draw the detected lines on the original frame
        if lines is not None:
            print("Red line detected")
            for line in lines:
                x1, y1, x2, y2 = line[0]  # Unpack line endpoints
                cv.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw line in green
        else:
            print("No red line detected")

        # Display the original frame with detected lines
        cv.imshow('Red Line Detection', frame)

        # # Get the bottom 100 pixels of the mask
        # bottom_region = mask[-100:, :]
        
        # # Find all non-zero (white) pixels in the bottom region
        # white_pixels = np.where(bottom_region > 0)
        
        # if len(white_pixels[1]) > 0:  # If any red pixels are found
        #     # Get leftmost (min x) and rightmost (max x) red points
        #     left_x = np.min(white_pixels[1])
        #     right_x = np.max(white_pixels[1])
            
        #     # Draw points on frame for visualization
        #     bottom_y = frame.shape[0] - 50  # Y coordinate in bottom region
        #     cv.circle(frame, (left_x, bottom_y), 5, (255, 0, 0), -1)   # Blue dot for leftmost
        #     cv.circle(frame, (right_x, bottom_y), 5, (0, 255, 0), -1)  # Green dot for rightmost
            
        #     print(f"Leftmost red x: {left_x}, Rightmost red x: {right_x}")
        # else:
        #     print("No red pixels found in bottom region")


        # Get the green mask pixels
        green_pixels = np.where(green_mask > 0)
        
        if len(green_pixels[1]) > 0:  # If any green pixels are found
            # Get leftmost (min x) and rightmost (max x) green points
            green_left_x = np.min(green_pixels[1])
            green_right_x = np.max(green_pixels[1])
            
            print(f"Leftmost green x: {green_left_x}, Rightmost green x: {green_right_x}")
        else:
            print("No green pixels found in frame")


        # Break loop on user interrupt (e.g., 'q' key press)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

# Run the function
detect_red_line()

