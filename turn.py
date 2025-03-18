from hardware import *

def get_distance(steps):
    global total_distance2
    revolutions = steps / 263
    total_distance2 = revolutions * WHEEL_CIRCUMFERENCE
    return total_distance2


try:
    left_steps = left_encoder.steps

    drive_motors(0.4, 0)

    while get_distance(abs(left_encoder.steps - left_steps)) < 26:
        continue

    stop_motors()

except KeyboardInterrupt:
    print("Program stopped")

finally:
    stop_motors()


