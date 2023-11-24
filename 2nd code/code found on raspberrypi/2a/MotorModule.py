# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 14:50:31 2022

@author: SpeciAl One 1-2
"""


import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
 
class Motor():
    def __init__(self,EnaA,In1A,In2A,EnaB,In1B,In2B):
        self.EnaA= EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB= EnaB
        self.In1B = In1B
        self.In2B = In2B
        GPIO.setup(self.EnaA,GPIO.OUT);GPIO.setup(self.In1A,GPIO.OUT);GPIO.setup(self.In2A,GPIO.OUT)
        GPIO.setup(self.EnaB,GPIO.OUT);GPIO.setup(self.In1B,GPIO.OUT);GPIO.setup(self.In2B,GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnaA, 100);
        self.pwmB = GPIO.PWM(self.EnaB, 100);
        self.pwmA.start(0);
        self.pwmB.start(0);
        self.mySpeed=0
 
    def move(self, speed=0.5, turn=0, t=0):
        speed *= 100
        turn *= 70        # todo: starnge value, need to check video
        leftSpeed = speed-turn
        rightSpeed = speed+turn
 
        if leftSpeed>100: leftSpeed =100
        elif leftSpeed<-100: leftSpeed = -100
        if rightSpeed>100: rightSpeed =100
        elif rightSpeed<-100: rightSpeed = -100
        # print(leftSpeed,rightSpeed)
        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))
        if leftSpeed>0:GPIO.output(self.In1A,GPIO.HIGH);GPIO.output(self.In2A,GPIO.LOW)
        else:GPIO.output(self.In1A,GPIO.LOW);GPIO.output(self.In2A,GPIO.HIGH)
        if rightSpeed>0:GPIO.output(self.In1B,GPIO.HIGH);GPIO.output(self.In2B,GPIO.LOW)
        else:GPIO.output(self.In1B,GPIO.LOW);GPIO.output(self.In2B,GPIO.HIGH)
        sleep(t)
 
    def stop(self,t=0):
        self.pwmA.ChangeDutyCycle(0);
        self.pwmB.ChangeDutyCycle(0);
        self.mySpeed=0
        sleep(t)
 
def main():
    motor.move(0.5, 0, 2)
    motor.stop(2)
    motor.move(-0.5, 0, 2)
    motor.stop(2)
    motor.move(0, 0.5, 2)
    motor.stop(2)
    motor.move(0, -0.5, 2)
    motor.stop(2)
 
if __name__ == '__main__':
    motor= Motor(2,3,4,17,22,27)
    main()
    '''
import RPi.GPIO as GPIO
from time import sleep
in1 = 3
in2 = 4
in3 = 22
in4 = 27
en = 18
en2 = 12
temp1 = 1
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
p1 = GPIO.PWM(en, 1000)
p1.start(50)
p2 = GPIO.PWM(en2, 4000)
p2.start(50)
print("r-run s-stop f-forward b-backward l-low m-medium h-high dm-frontmiddle dr-frontright dl-frontleft e-exit")
def frontmiddle():
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
def frontright():
    p2.ChangeDutyCycle(100)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
def frontleft():
    p2.ChangeDutyCycle(100)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
def forward(speed=50,time=0):
    p1.ChangeDutyCycle(speed)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    frontmiddle()
    sleep(time)
def backward(speed=50,time=0):
    p1.ChangeDutyCycle(speed)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    frontmiddle()
    sleep(time)
def stop(time=0):
    frontmiddle()
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    sleep(time)
def fright(speed=50,time=0):
    forward(speed)
    frontright()
    sleep(time)
def fleft(speed=50,time=0):
    forward(speed)
    frontleft()
    sleep(time)
def bright(speed=50,time=0):
    backward(speed)
    frontright()
    sleep(time)
def bleft(speed=50,time=0):
    backward(speed)
    frontleft()
    sleep(time)
    '''