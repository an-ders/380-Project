
# -------- DRIVE TRAIN -----------

def drive(left, right):
    return

def drive_forward():
     motors_forward(0.25)
     return

def drive_backward():
     motors_backward(0.25)
     return

def stop():
     motors_stop()
     return

def turn(angle):
     turn_left(0.25)
     return


# ----------- GRABBER -------------

def pickup():
     return

def drop():
     return

from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep

IN1 = DigitalOutputDevice(17); # GPIO 17 (Pin 11) -> Motor 1 Forward
IN2 = DigitalOutputDevice(27); # GPIO 27 (Pin 13) -> Motor 1 Backward
IN3 = DigitalOutputDevice(23); # GPIO 23 (Pin 16) -> Motor 2 Forward
IN4 = DigitalOutputDevice(24); # GPIO 24 (Pin 18) -> Motor 2 Backward
ENA = PWMOutputDevice(12); # GPIO 12 (Pin 32) -> PWM for Motor A (PWM0)
ENB = PWMOutputDevice(13); # GPIO 13 (Pin 33) -> PWM for Motor B (PWM1)

# PWM Frequency
# PWM_FREQ = 1000

# Setup GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(IN1, GPIO.OUT)
# GPIO.setup(IN2, GPIO.OUT)
# GPIO.setup(IN3, GPIO.OUT)
# GPIO.setup(IN4, GPIO.OUT)
# GPIO.setup(ENA, GPIO.OUT)
# GPIO.setup(ENB, GPIO.OUT)

# Setup PWM
# pwm_motorA = GPIO.PWM(ENA, PWM_FREQ)
# pwm_motorB = GPIO.PWM(ENB, PWM_FREQ)
# pwm_motorA.start(0);
# pwm_motorB.start(0);

def motorA_forward(speed):
    IN1.on()
    IN2.off()
    ENA.value = speed

def motorA_backward(speed):
    IN1.off()
    IN2.on()
    ENA.value = speed

def motorB_forward(speed):
    IN3.on()
    IN4.off()
    ENB.value = speed
    
def motorB_backward(speed):
    IN3.off()
    IN4.on()
    ENB.value = speed

def motorA_stop():
    IN1.off()
    IN2.off()
    ENA.value = 0
    
def motorB_stop():
    IN3.off()
    IN4.off()
    ENB.value = 0

def motors_forward(speed):
    motorA_forward(speed);
    motorB_forward(speed);

def motors_backward(speed):
    motorA_backward(speed);
    motorB_backward(speed);

def turn_left(speed):
    motorA_backward(speed);
    motorB_forward(speed);

def turn_right(speed):
    motorA_forward(speed);
    motorB_backward(speed);
    
def motors_stop():
    motorA_stop()
    motorB_stop()

# def motors_forward(speed):
#     # Move both motors forward
#     GPIO.output(IN1, GPIO.HIGH)
#     GPIO.output(IN2, GPIO.LOW)
#     GPIO.output(IN3, GPIO.HIGH)
#     GPIO.output(IN4, GPIO.LOW)
#     pwm_motorA.ChangeDutyCycle(speed)
#     pwm_motorB.ChangeDutyCycle(speed)

# def motors_backward(speed):
#     # Move both motors backward
#     GPIO.output(IN1, GPIO.LOW)
#     GPIO.output(IN2, GPIO.HIGH)
#     GPIO.output(IN3, GPIO.LOW)
#     GPIO.output(IN4, GPIO.HIGH)
#     pwm_motorA.ChangeDutyCycle(speed)
#     pwm_motorB.ChangeDutyCycle(speed) 

# def motors_stop():
#     # Stop both motors
#     GPIO.output(IN1, GPIO.LOW)
#     GPIO.output(IN2, GPIO.LOW)
#     GPIO.output(IN3, GPIO.LOW)
#     GPIO.output(IN4, GPIO.LOW)
#     pwm_motorA.ChangeDutyCycle(0)
#     pwm_motorB.ChangeDutyCycle(0) 

# def motor_turn_left():
#     # Turn left: Motor 1 backward, Motor 2 forward
#     GPIO.output(IN1, GPIO.LOW)
#     GPIO.output(IN2, GPIO.HIGH)
#     GPIO.output(IN3, GPIO.HIGH)
#     GPIO.output(IN4, GPIO.LOW)
# 
# def motor_turn_right():
#     # Turn right: Motor 1 forward, Motor 2 backward
#     GPIO.output(IN1, GPIO.HIGH)
#     GPIO.output(IN2, GPIO.LOW)
#     GPIO.output(IN3, GPIO.LOW)
#     GPIO.output(IN4, GPIO.HIGH)

# try:
#     while True:
#         print("Moving A forward")
#         motors_forward(0.5)
#         sleep(2)

#         print("Moving B forward")
#         motors_backward(0.25)
#         sleep(2)
        
#         print("Stopping")
#         motors_stop()
#         sleep(2)

# #         print("Turning left")
# #         motor_turn_left()
# #         time.sleep(2)
# # 
# #         print("Turning right")
# #         motor_turn_right()
# #         time.sleep(2)

# #         print("Stopping")   
# #         motors_stop()
# #         time.sleep(2)

# except KeyboardInterrupt:
#     print("Program stopped")

# finally:
#     motorA_stop()
#     motorB_stop()
#     IN1.close()
#     IN2.close()
#     IN3.close()
#     IN4.close()
#     ENA.close()
#     ENB.close()

