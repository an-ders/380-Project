from hardware import *
from time import sleep
import PID
import platform
import cv2 as cv
import numpy as np

FRAME_BOTTOM = 679  # y value of bottom row of pixels
PIXEL_DIST = 50  # pixel distance from top of target to center  # TODO tune me
SLEEP_TIME = 2

def get_dist_to_target(edges):
    # Get the coordinates of all non-zero (edge) pixels
    edge_points = np.column_stack(np.where(edges > 0))

    if edge_points.size == 0:
        return None  # No edges found

    # edge_points[:, 0] is row (y), edge_points[:, 1] is column (x)
    topmost_y = int(edge_points[:, 0].min())
    pixel_dist = FRAME_BOTTOM - (topmost_y + PIXEL_DIST)
    return pixel_dist

def pick_up_lego_person_main():
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

    pid = PID.PID()
    dist_to_target = 1000  # arbitrary large number
    # Assumes that top of target is in sight
    # TODO is camera wide enough for target sight?
    while dist_to_target > 0:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, BLUE_HSV_RANGE['lower'], BLUE_HSV_RANGE['upper'])
        blue_regions = cv.bitwise_and(frame, frame, mask=mask)
        gray = cv.cvtColor(blue_regions, cv.COLOR_BGR2GRAY)
        edges = cv.Canny(gray, 50, 150)
        
        dist_to_target = get_dist_to_target(edges)
        pid.get_offset(hsv, native_width, "b")
        pid.calculate_control_signal()
        left_duty_cycle, right_duty_cycle = pid.get_differential_speed()
        drive_motors(left_duty_cycle, right_duty_cycle)
        # TODO this should probably be slower^

        # Display the original frame with detected lines
        cv.imshow('Red Line Detection', frame)

        # Break loop on user interrupt (e.g., 'q' key press)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    sleep(SLEEP_TIME)
    lower_arm()
    sleep(SLEEP_TIME)
    raise_arm()
    sleep(SLEEP_TIME)
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    pick_up_lego_person_main()