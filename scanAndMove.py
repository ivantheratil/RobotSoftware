#Libraries
import RPi.GPIO as GPIO
import time
import os
import keyboard


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO_TRIGGER1 = 22
GPIO_ECHO1 = 23

in1 = 20
in2 = 26
en = 19
temp1 = 1


#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,250)

def distance(gptrig, gpecho):
    # set Trigger to HIGH
    GPIO.output(gptrig, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.01)
    GPIO.output(gptrig, False)

    while GPIO.input(gpecho) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(gpecho) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2

    return distance

#Media Functions
def pp():
    keyboard.press_and_release(' ')
def forwards():
    keyboard.press_and_release('right')
def backwards():
    keyboard.press_and_release('left')
def clr():
    print("\n" * 40)

#0 = Undetected, 1 = Left Detected, 2 = Right Detected
state = 0
delta1 = time.time()

pwr = 50
p.start(pwr)
if __name__ == '__main__':
    try:
        os.system('clear')
        while True:
            #Determines time passed
            if round(time.time(), 0 ) == round(time.time(), 2):
                dist2 = distance(GPIO_TRIGGER1, GPIO_ECHO1)
                dist1 = distance(GPIO_TRIGGER, GPIO_ECHO)
                os.system('clear')
                print ("Sensor #1: " + str(round(dist1,2)) + " | Sensor #2: " + str(round(dist2,2)) + " | Power: " + str(pwr))
            #Initial detection
            if keyboard.is_pressed('f'):
                os.system('clear')
                print ("Sensor #1: " + str(round(dist1,2)) + " | Sensor #2: " + str(round(dist2,2)) + " | Power: " + str(pwr))
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
            elif keyboard.is_pressed('r'):
                os.system('clear')
                print ("Sensor #1: " + str(round(dist1,2)) + " | Sensor #2: " + str(round(dist2,2)) + " | Power: " + str(pwr))
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
            elif keyboard.is_pressed("i"):
                if pwr < 100:
                    pwr += 25
                    os.system('clear')
                    print("Power Multiplier: " + str(pwr))
                    p.ChangeDutyCycle(pwr)
                    time.sleep(0.5)
            elif keyboard.is_pressed("k"):
                if pwr > 0:
                    pwr -= 25
                    os.system('clear')
                    print("Power Multiplier: " + str(pwr))
                    p.ChangeDutyCycle(pwr)
                    time.sleep(0.5)
            else:
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User") 
        GPIO.cleanup()





