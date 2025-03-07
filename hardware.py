from constants import *
from test_classes import *
from gpiozero import PWMOutputDevice, DigitalOutputDevice

IN1 = TestDevice(17)  # GPIO 17 (Pin 11) -> Motor 1 Forward
IN2 = TestDevice(27)  # GPIO 27 (Pin 13) -> Motor 1 Backward
IN3 = TestDevice(23)  # GPIO 23 (Pin 16) -> Motor 2 Forward
IN4 = TestDevice(24)  # GPIO 24 (Pin 18) -> Motor 2 Backward
ENA = TestDevice(12)  # GPIO 12 (Pin 32) -> PWM for Motor A (PWM0)
ENB = TestDevice(13)  # GPIO 13 (Pin 33) -> PWM for Motor B (PWM1)

if ENV != "TEST":
    IN1 = DigitalOutputDevice(17)  # GPIO 17 (Pin 11) -> Motor 1 Forward
    IN2 = DigitalOutputDevice(27)  # GPIO 27 (Pin 13) -> Motor 1 Backward
    IN3 = DigitalOutputDevice(23)  # GPIO 23 (Pin 16) -> Motor 2 Forward
    IN4 = DigitalOutputDevice(24)  # GPIO 24 (Pin 18) -> Motor 2 Backward
    ENA = PWMOutputDevice(12)  # GPIO 12 (Pin 32) -> PWM for Motor A (PWM0)
    ENB = PWMOutputDevice(13)  # GPIO 13 (Pin 33) -> PWM for Motor B (PWM1)

MAX_SPEED = 0.6

# -------- DRIVE TRAIN -----------


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
        print("Error: Setting speed is too high")
        return

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
        print("Error: Setting speed is too high")
        return

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


def pickup():
    return


def drop():
    return
