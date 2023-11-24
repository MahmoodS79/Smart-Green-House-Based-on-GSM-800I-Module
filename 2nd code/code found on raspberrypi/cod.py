import RPi.GPIO as gpio
import time
import sys
import tkinter as tk
from tkinter import Label

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(15, gpio.OUT)
gpio.setup(14, gpio.OUT)

pwm = gpio.PWM(15, 50)
pwm_up = gpio.PWM(14, 50)

pwm.start(0)
pwm_up.start(0)

def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)

def forward(tf):
    gpio.output(17, False)
    gpio.output(22, True) 
    gpio.output(23, False) 
    gpio.output(24, True) 
    time.sleep(tf)
    gpio.cleanup()

def reverse (tf):
    gpio.output(17, True)
    gpio.output(22, False) 
    gpio.output(23, True) 
    gpio.output(24, False) 
    time.sleep(tf)
    gpio.cleanup()

def turn_left(tf):
    gpio.output(17, True)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(tf)
    gpio.cleanup()    
    
def turn_right(tf):
    gpio.output(17, False) 
    gpio.output(22, True) 
    gpio.output(23, False)
    gpio.output(24, False)
    time.sleep(tf)
    gpio.cleanup()    
    
def pivot_left(tf):
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(tf)
    gpio.cleanup()    
    
def pivot_right(tf):
    gpio.output(17, False) 
    gpio.output(22, True) 
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(tf)
    gpio.cleanup()
    
def SetAngle(angle):
    pwm.start(0)
    duty = angle / 18 + 2
    gpio.output(15, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    gpio.output(15, False)
    pwm.ChangeDutyCycle(0)
    
SetAngle(100)

def SetAngle_up(angle):
    pwm_up.start(0)
    duty = angle / 18 + 2
    gpio.output(14, True)
    pwm_up.ChangeDutyCycle(duty)
    time.sleep(1)
    gpio.output(14, False)
    pwm_up.ChangeDutyCycle(0)

#servo controls
def cam_left(event):
    key_press = event.char
    print("Key: ", event.char)
    SetAngle(180)
    time.sleep(0.3)
    #gpio.cleanup()

def cam_right(event):
    key_press = event.char
    print("Key: ", event.char)
    SetAngle(25)
    time.sleep(0.3)

def cam_straight(event):
    key_press = event.char
    print('Key: ', event.char)
    SetAngle(100)
    time.sleep(0.3)

def cam_up(event):
    key_press = event.char
    print('Key: ', event.char)
    SetAngle_up(10)
    time.sleep(0.3)
    
def cam_down(event):
    key_press = event.char
    print('Key: ', event.char)
    SetAngle_up(70)
    time.sleep(0.3)

def cam_level(event):
    key_press = event.char
    print('Key: ', event.char)
    SetAngle_up(50)
    time.sleep(0.3)    

def key_input(event):
    init()
    print('Key:', event.char)
    key_press = event.char
    sleep_time = 0.030
    
    if key_press.lower() == 'w':
        forward(sleep_time)
    elif key_press.lower() == 's':
        reverse(sleep_time)
    elif key_press.lower() == 'a':
        turn_left(sleep_time)
    elif key_press.lower() == 'd':
        turn_right(sleep_time)
    elif key_press.lower() == 'q':
        pivot_left(sleep_time)
    elif key_press.lower() == 'e':
        pivot_right(sleep_time)
    else:
        gpio.cleanup()
        
command = tk.Tk()
command.bind('<KeyPress>', key_input)
command.bind('j', cam_left)
command.bind('l', cam_right)
command.bind('k', cam_straight)
command.bind('i', cam_up)
command.bind('k', cam_level)
command.bind('m', cam_down)
command.mainloop()