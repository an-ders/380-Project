from source.follow_line import follow_line
from source.pickup import pickup
import platform
import cv2 as cv

if __name__ == "__main__":
    if platform.system() == 'Windows':
        cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    else:
        cap = cv.VideoCapture(0)

    # cap.set(cv.CAP_PROP_FRAME_WIDTH, SCREEN_WIDTH)
    # cap.set(cv.CAP_PROP_FRAME_HEIGHT, SCREEN_HEIGHT)

    follow_line(cap)

    pickup(cap)

    follow_line(cap)

    cap.release()
