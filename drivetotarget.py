import cv2 as cv
from hardware import *
import platform
import PID

KP = 0.0003  # Proportional gain
KI = 0.0  # Integral gain
KD = 0.00025  # Derivative gain

base_speed = 0.2

def drive_to_target_main():
    # Initialize webcam
    if platform.system() == 'Windows':
        cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    else:
        cap = cv.VideoCapture(0)

    error = 0
    derivative = 0
    previous_error = 0
    
    started = False
    numTurns = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # Convert to HSV color space
        mask1 = cv.inRange(hsv, RED_HSV_RANGE['lower_red1'], RED_HSV_RANGE['upper_red1'])  # Create masks for red color
        mask2 = cv.inRange(hsv, RED_HSV_RANGE['lower_red2'], RED_HSV_RANGE['upper_red2'])  # Create masks for red color

        mask = cv.bitwise_or(mask1, mask2)  # get all red

        c, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        if c:
            x = findMiddle(c)

            if x < 0: continue;

            error = (1280 // 2) - x
            
            if abs(error) < 50: continue
            
            derivative = error - previous_error
            
            signal = (KP * error) + (KD * derivative)
            previous_error = error

            left_speed = base_speed - signal
            right_speed = base_speed + signal
            
            print(f"{left_speed:.3f}, {right_speed:.3f}")
            drive_motors(left_speed, right_speed)

        elif started and numTurns == 0:
            numTurns += 1
            drive_motors(0.15, -0.15)
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to capture frame")
                    break

                hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # Convert to HSV color space
                mask1 = cv.inRange(hsv, RED_HSV_RANGE['lower_red1'], RED_HSV_RANGE['upper_red1'])  # Create masks for red color
                mask2 = cv.inRange(hsv, RED_HSV_RANGE['lower_red2'], RED_HSV_RANGE['upper_red2'])  # Create masks for red color

                mask = cv.bitwise_or(mask1, mask2)  # get all red

                c, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

                if c:
                    x = findMiddle(c)

                    if x < 0: continue;

                    error = (1280 // 2) - x
                    
                    if abs(error) < 200: break
            sleep(2)
        else:
            stop_motors()
            break

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

def findMiddle(c):
    c = max(c, key=cv.contourArea)
    mom = cv.moments(c)

    if mom["m00"]:
        started = True
        return int(mom["m10"] / mom["m00"])

    return -1

if __name__ == "__main__":
    drive_to_target_main()