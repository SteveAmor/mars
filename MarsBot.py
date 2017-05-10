#!/usr/bin/env python
# coding: Latin-1
# Original code from https://github.com/Coretec-Robotics/Tiny_4wd
# Load library functions we want

from inputs import get_gamepad
from gpiozero import Motor
from gpiozero import Buzzer
from os import system
from time import sleep

def mixer(inYaw, inThrottle,):
    left = inThrottle + inYaw
    right = inThrottle - inYaw
    scaleLeft = abs(left / 125.0)
    scaleRight = abs(right / 125.0)
    scaleMax = max(scaleLeft, scaleRight)
    scaleMax = max(1, scaleMax)
    out_left = int(constrain(left / scaleMax, -125, 125))
    out_right = int(constrain(right / scaleMax, -125, 125))
    results = [out_right, out_left]
    return results

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

# Setup
maxPower  = 1.0
power_left = 0.0
power_right = 0.0
x_axis = 0.0
y_axis = 0.0

rightMotor = Motor(20,21)
leftMotor = Motor(16,19)
buzzer = Buzzer(13)

try:
    print('Press CTRL+C to quit')

    # Loop indefinitely
    while True:

        events = get_gamepad()
        for event in events:
            print(event.code, event.state)
            if event.code == "ABS_Y":
                if event.state > 130:
                    print("Backwards")
                elif event.state < 125:
                    print("Forward")
                y_axis = event.state
                if y_axis > 130:
                    y_axis = -(y_axis - 130)
                elif y_axis < 125:
                    y_axis = ((-y_axis) + 125)
                else:
                    y_axis = 0.0
                print("Y: " + str(-y_axis))
            if event.code == "ABS_Z":
                if event.state > 130:
                    print("Right")
                elif event.state < 125:
                    print("Left")
                x_axis = event.state
                if x_axis > 130:
                    x_axis = (x_axis - 130)
                elif x_axis < 125:
                    x_axis = -((-x_axis) + 125)
                else:
                    x_axis = 0.0
                print("X: " + str(x_axis))

            if event.code == "BTN_TL":
                if event.state == True:
                    print("Botton Left")
            if event.code == "BTN_TR":
                if event.state == True:
                    print("Botton Right")
            if event.code == "BTN_Z":
                if event.state == True:
                    print("Top right")

            if event.code == "BTN_WEST":
                if event.state == True:
                    print("Top left")

            if event.code == "BTN_TL2":
                if event.state == True:
                    print("Select")
                    for i in range(5):
                        buzzer.on()
                        sleep(0.5)
                        buzzer.off()
                        sleep(0.5)
                    system("sudo shutdown now")


                    x_axis = 0
                    y_axis = 0
            if event.code == "ABS_HAT0X":
                if event.state == -1:
                    print("D pad Left")

                elif event.state == 1:
                    print("D pad Right")

            if event.code == "ABS_HAT0Y":

                if event.state == -1:

                    print("D pad Up")


                elif event.state == 1:

                    print("D pad Down")


            mixer_results = mixer(x_axis, y_axis)
            #print (mixer_results)
            power_left = (mixer_results[1] / 125.0)
            power_right = (mixer_results[0] / 125.0)

            print("left: " + str(power_left) + " right: " + str(power_right))


            if(power_left > 0):
                leftMotor.forward(speed=power_left)
            elif(power_left < 0):
                leftMotor.backward(speed=-power_left)
            else:
                leftMotor.stop()

            if(power_right > 0):
               rightMotor.forward(speed=power_right)
            elif(power_right < 0):
                rightMotor.backward(speed=-power_right) 
            else:
                rightMotor.stop()


            print(event.ev_type, event.code, event.state)


except KeyboardInterrupt:

    # CTRL+C exit, disable all drives
    print("stop")
    rightMotor.stop()
    leftMotor.stop()
print("bye")
