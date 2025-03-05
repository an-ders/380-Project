import cv2 as cv
import numpy as np
import time
from constants import *


def main():
    # Initialize webcam
    cap = cv.VideoCapture(0)

    # Set video parameters
    native_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    native_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    # Set video parameters
    cap.set(cv.CAP_PROP_FRAME_WIDTH, native_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, native_height)
    cap.set(cv.CAP_PROP_FPS, FPS)

    # Define HSV ranges for colors
    # Red has two ranges due to how it wraps around in HSV

    while True:
        # Add a delay to control frame rate (e.g., 10 FPS)
        time.sleep(1/FPS)

        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Resize frame for consistency
        frame = cv.resize(frame, (native_width, native_height))

        # Convert to HSV color space
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Create masks for each color
        # Red (combining two ranges)
        # red_mask1 = cv.inRange(hsv, red_ranges[0]['lower'], red_ranges[0]['upper'])
        # red_mask2 = cv.inRange(hsv, red_ranges[1]['lower'], red_ranges[1]['upper'])

        # red_mask = cv.bitwise_or(red_mask1, red_mask2)
        red_mask = cv.inRange(
            hsv, RED_HSV_RANGE['lower'], RED_HSV_RANGE['upper'])
        green_mask = cv.inRange(
            hsv, GREEN_HSV_RANGE['lower'], GREEN_HSV_RANGE['upper'])
        blue_mask = cv.inRange(
            hsv, BLUE_HSV_RANGE['lower'], BLUE_HSV_RANGE['upper'])

        # Apply mask to isolate green regions
        red_regions = cv.bitwise_and(frame, frame, mask=red_mask)
        green_regions = cv.bitwise_and(frame, frame, mask=green_mask)
        blue_regions = cv.bitwise_and(frame, frame, mask=blue_mask)

        # [*4] Apply Canny edge detection
        # edges = cv.Canny(gray, 50, 150)

        # [*5] Use HoughLinesP to detect line segments
        # lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

        # Draw the detected lines on the original frame
        # if lines is not None:
        #     print("Red line detected")
        #     for line in lines:
        #         x1, y1, x2, y2 = line[0]  # Unpack line endpoints
        #         cv.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw line in green
        # else:
        #     print("No red line detected")

        # Display the original frame with detected lines

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

        # -------------------------  GREEN ---------------------------------------------------

        # Mask off top 100 pixels for both masks
        green_mask[:100, :] = 0
        # Keep only bottom 100 pixels (frame height is 480)
        red_mask[:FRAME_HEIGHT - 100, :] = 0

        # Draw horizontal lines showing masked regions
        # Top green mask line at y=100
        cv.line(frame, (0, 100), (frame.shape[1], 100), (0, 255, 0), 2)
        # Bottom red mask line at y=380
        cv.line(frame, (0, 380), (frame.shape[1], 380), (0, 0, 255), 2)

        # Find green pixels
        green_pixels = np.where(green_mask > 0)
        # Find red pixels
        red_pixels = np.where(red_mask > 0)

        if len(green_pixels[1]) > 0:  # If any green pixels are found
            # Get leftmost (min x) and rightmost (max x) green points
            green_left_x = np.min(green_pixels[1])
            green_right_x = np.max(green_pixels[1])

            # Get highest (min y) and lowest (max y) green points
            green_top_y = np.min(green_pixels[0])
            green_bottom_y = np.max(green_pixels[0])

            # Draw vertical green lines at min and max x values
            cv.line(frame, (green_left_x, 0), (green_left_x,
                    frame.shape[0]), (0, 255, 0), 2)  # Left line in green
            cv.line(frame, (green_right_x, 0), (green_right_x,
                    frame.shape[0]), (0, 255, 0), 2)  # Right line in green

            #     print(f"Leftmost green x: {green_left_x}, Rightmost green x: {green_right_x}")
            #     print(f"Highest green y: {green_top_y}, Lowest green y: {green_bottom_y}")
            # else:
            #     print("No green pixels found in frame")

        if len(red_pixels[1]) > 0:  # If any red pixels are found
            # Get leftmost (min x) and rightmost (max x) red points
            red_left_x = np.min(red_pixels[1])
            red_right_x = np.max(red_pixels[1])

            # Draw vertical red lines at min and max x values
            cv.line(frame, (red_left_x, 0), (red_left_x,
                    frame.shape[0]), (0, 0, 255), 2)  # Left line in red
            cv.line(frame, (red_right_x, 0), (red_right_x,
                    frame.shape[0]), (0, 0, 255), 2)  # Right line in red

        cv.imshow('Red Line Detection', frame)

        # Break loop on user interrupt (e.g., 'q' key press)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


# Run the function
main()
