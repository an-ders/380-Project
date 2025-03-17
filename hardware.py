from constants import *
from test_classes import *
from gpiozero import PWMOutputDevice, DigitalOutputDevice, RotaryEncoder
from time import time, sleep

ENV = "TEST"

IN1 = TestDevice(17)  # GPIO 17 (Pin 11) -> Motor 1 Forward
IN2 = TestDevice(27)  # GPIO 27 (Pin 13) -> Motor 1 Backward
IN3 = TestDevice(23)  # GPIO 23 (Pin 16) -> Motor 2 Forward
IN4 = TestDevice(24)  # GPIO 24 (Pin 18) -> Motor 2 Backward
ENA = TestDevice(12)  # GPIO 12 (Pin 32) -> PWM for Motor A (PWM0)
ENB = TestDevice(13)  # GPIO 13 (Pin 33) -> PWM for Motor B (PWM1)
encoder1 = TestEncoder(5, 6)
encoder2 = TestEncoder(16, 26)


if ENV != "TEST":
    IN1 = DigitalOutputDevice(17)  # GPIO 17 (Pin 11) -> Motor 1 Forward
    IN2 = DigitalOutputDevice(27)  # GPIO 27 (Pin 13) -> Motor 1 Backward
    IN3 = DigitalOutputDevice(23)  # GPIO 23 (Pin 16) -> Motor 2 Forward
    IN4 = DigitalOutputDevice(24)  # GPIO 24 (Pin 18) -> Motor 2 Backward
    ENA = PWMOutputDevice(12)  # GPIO 12 (Pin 32) -> PWM for Motor A (PWM0)
    ENB = PWMOutputDevice(13)  # GPIO 13 (Pin 33) -> PWM for Motor B (PWM1)
    encoder1 = RotaryEncoder(5, 6)  # Encoder 1 (A=5, B=6)
    encoder2 = RotaryEncoder(16, 26)  # Encoder 1 (A=16, B=26)

MAX_VOLTAGE = 12
MOTOR_VOLTAGE = 7
MAX_SPEED = MOTOR_VOLTAGE / MAX_VOLTAGE

WHEEL_D = 0.067
WHEEL_CIRCUMFERENCE = 3.14159 * WHEEL_D

COUNTS_PER_REV = 14
GEAR_RATIO = 20.4
COUNTS_PER_OUT_REV = COUNTS_PER_REV * GEAR_RATIO

# -------- DRIVE TRAIN -----------
# Function to calculate speed for Motor 1


def right_motor_speed():
    global last_time1, last_count1
    current_time = time()
    current_count = encoder1.steps

    # Calculate speed
    delta_time = current_time - last_time1
    delta_count = current_count - last_count1
    if delta_time > 0:
        revolutions = delta_count / COUNTS_PER_OUT_REV
        distance = revolutions * WHEEL_CIRCUMFERENCE
        speed = distance / delta_time
    else:
        speed = 0

    # Update last time and last count
    last_time1 = current_time
    last_count1 = current_count

    return speed

# Function to calculate speed for Motor 2


def left_motor_speed():
    global last_time2, last_count2
    current_time = time()
    current_count = encoder2.steps

    # Calculate speed
    delta_time = current_time - last_time2
    delta_count = current_count - last_count2
    if delta_time > 0:
        revolutions = delta_count / COUNTS_PER_OUT_REV
        distance = revolutions * WHEEL_CIRCUMFERENCE
        speed = distance / delta_time
    else:
        speed = 0

    # Update last time and last count
    last_time2 = current_time
    last_count2 = current_count

    return speed

# Function to calculate distance for Motor 1


def right_motor_distance():
    global total_distance1
    current_count = encoder1.steps
    revolutions = current_count / COUNTS_PER_OUT_REV
    total_distance1 = revolutions * WHEEL_CIRCUMFERENCE
    return total_distance1

# Function to calculate distance for Motor 2


def left_motor_distance():
    global total_distance2
    current_count = encoder2.steps
    revolutions = current_count / COUNTS_PER_OUT_REV
    total_distance2 = revolutions * WHEEL_CIRCUMFERENCE
    return total_distance2

# Function to calculate rotation in degrees for Motor 1


def right_motor_rotation():
    current_count = encoder1.steps
    rotation_degrees = (current_count / COUNTS_PER_OUT_REV) * 360
    return rotation_degrees

# Function to calculate rotation in degrees for Motor 2


def left_motor_rotation():
    current_count = encoder2.steps
    rotation_degrees = (current_count / COUNTS_PER_OUT_REV) * 360
    return rotation_degrees


def drive_motors(left_speed, right_speed):
    drive_left_motor(left_speed)
    drive_right_motor(right_speed)


def drive_motors(speed):
    drive_left_motor(speed)
    drive_right_motor(speed)


def stop_motors():
    stop_right_motor()
    stop_left_motor()


def turn(angle):
    return


def drive_right_motor(speed):
    if abs(speed) > MAX_SPEED:
        speed = MAX_SPEED

    if speed == 0:
        stop_right_motor()
    elif speed < 0:
        IN1.off()
        IN2.on()
    else:
        IN1.on()
        IN2.off()

    ENA.value = abs(speed)


def drive_left_motor(speed):
    if abs(speed) > MAX_SPEED:
        speed = MAX_SPEED

    if speed == 0:
        stop_left_motor()
    elif speed < 0:
        IN3.off()
        IN4.on()
    else:
        IN3.on()
        IN4.off()

    ENA.value = abs(speed)


def stop_right_motor():
    IN1.off()
    IN2.off()
    ENA.value = 0


def stop_left_motor():
    IN3.off()
    IN4.off()
    ENB.value = 0

# ----------- GRABBER -------------


def lower_arm():  # TODO by Shreya
    return


def raise_arm():  # TODO by Shreya
    return


# ------ TEST SCRIPT ------------

if ENV != "TEST":
    try:
        while True:
            print("Moving B forward")
            drive_motors(0.2)
            sleep(2)

            # Get encoder data for Motor 1
            speed1 = right_motor_speed()
            distance1 = right_motor_distance()
            rotation1 = right_motor_rotation()
            print(
                f"Motor 1: Speed = {speed1:.2f} m/s, Distance = {distance1:.2f} m, Rotation = {rotation1:.2f}Â°")

            # Get encoder data for Motor 2
            speed2 = left_motor_speed()
            distance2 = left_motor_distance()
            rotation2 = left_motor_rotation()
            print(
                f"Motor 2: Speed = {speed2:.2f} m/s, Distance = {distance2:.2f} m, Rotation = {rotation2:.2f}Â°")

            print("Stopping")
            stop_motors()
            sleep(2)

    except KeyboardInterrupt:
        print("Program stopped")

    finally:
        stop_motors()
        IN1.close()
        IN2.close()
        IN3.close()
        IN4.close()
        ENA.close()
        ENB.close()
