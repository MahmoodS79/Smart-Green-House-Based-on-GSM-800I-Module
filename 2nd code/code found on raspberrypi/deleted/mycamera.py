from picamera import PiCamera
import time
width = 800
height = 600
camera = PiCamera()
camera.start_preview()
time.sleep(2)


camera.capture('myfile.jpg')