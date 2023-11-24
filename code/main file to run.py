import RPi.GPIO as GPIO
import ADC0834
import serial
import time
import datetime
import Adafruit_DHT
from MQ135 import mq135
from GSM import SIM800L
import pyrebase


#mailing and recording
import os
import smtplib, email.utils
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
#from picamera import PiCamera

config = {
  "apiKey": "AIzaSyCqGcmWnclvw2aU4EL9XaqAX5HJ6FiVdv0",
  "authDomain": "greenhouse-bcd96.firebaseapp.com",
  "databaseURL": "https://greenhouse-bcd96-default-rtdb.firebaseio.com",
  "storageBucket": "greenhouse-bcd96.appspot.com"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
database = firebase.database()

#setup stage
temp_sensor = Adafruit_DHT.DHT11
dht11_pin = 22 #(BCM) or 10
fan = 26   # (BCM)
water_pump = 19
gas_sensor = 25
ON_OFF_sensor = 16 #(BCM)q
sim800l=SIM800L('/dev/ttyS0')
prev_time1=0
prev_time2=0
flag1=0
flag2=0
not_num='01552896977'
count=1
list_representing_all_IDs_beenRead_by_gsm=[]
        #mailing and recording
#camera Basic initialization
path="/home/pi/Desktop/"
name="test"
ext=".h264"
name_count=0
#mails
subject='recording has been requested'
bodyText="""
recording has been requested
"""
SMTP_SERVER='smtp.gmail.com'
SMTP_PORT=587
USERNAME="mahmood7ali9@gmail.com"
PASSWORD="ennmhwpymzcinyge"
RECIEVER_EMAIL="sence79.s7.s9@gmail.com"

#Initializing GPIO
ADC0834.setup()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(fan,GPIO.OUT)
GPIO.setup(water_pump,GPIO.OUT)

'''GPIO.setup(ON_OFF_sensor, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
def Restart(channel):
   os.system("sudo shutdown -r now")
GPIO.add_event_detect(ON_OFF_sensor, GPIO.FALLING, callback = Restart)
'''
sim800l.command('AT+CMGDA="DEL ALL"\n')
time.sleep(3)
sim800l.command('AT+CMGF=1'+'\r\n')
time.sleep(0.5)
   #mailing and recording
#camera Basic initialization
#camera = PiCamera()
#camera.resolution = (1024,720)
#camera.brightness = 70

TimeStamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open('filename.csv', 'a') as f:
        print('Moisture,Tempreture,Humidtity,Brightness,AirQuality, TimeStamp', file=f)

def ____output(out):
    with open('filename.csv', 'a') as f:
        print(out,',',TimeStamp,file=f)

def remove_file():
    if os.path.exists(path+name+str(name_count)+ext):
        os.remove(path+name+str(name_count)+ext)
    else:
        print("file does not exist")

def send_mail():
    #holds the body, recipient, transmitter and header
    message=MIMEMultipart()
    message["From"]=email.utils.formataddr(("PI",USERNAME))
    message["To"]=email.utils.formataddr(("Recipient",RECIEVER_EMAIL))
    message["Subject"]=subject
    message.attach(MIMEText(bodyText, 'plain'))
     
     #holds the path, the name and the extension of the picture or video
    attachment=open(path+name+str(name_count)+ext, "rb")

     #encodes and encrypts the picture or the video   
    mimeBase=MIMEBase('application','octet-stream')
    mimeBase.set_payload((attachment).read())
    encoders.encode_base64(mimeBase)
    mimeBase.add_header('Content-Disposition', "attachment; filename= " +(name+str(name_count)+ext))

    #transforming data into bytes and bits and attaching it to message
    message.attach(mimeBase)
    text=message.as_string()

     #sends the email to the recipient and managing the sending and the allowance 
    server=smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(USERNAME, PASSWORD)
    server.sendmail(USERNAME, RECIEVER_EMAIL, text)
    server.quit
    print("Email sent")

             
try:
      print('Moisture,Temp,Humidtity,Brightness,AirQuality, TimeStamp')
      while True:
            gas = mq135(ADC0834.getResult(0))
            gas_mesurement = gas.get_ppm()
            humid , temp = Adafruit_DHT.read_retry(temp_sensor, dht11_pin)
            moist = ADC0834.getResult(1)
            Brightness = ADC0834.getResult(2)
            TimeStamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time.sleep(10) 
            if(humid is not None and temp is not None):
                output = '{0:7.2f},{1:4.2f},{2:8.2f},{3:9f},{4:9f},{5}'
                output = output.format(moist, temp, humid, Brightness, gas_mesurement, TimeStamp)
                print(output)
                ____output(output)
                            #the actions based on measurements____________________________________________
            
                if((time.time() - prev_time1 >120 ) or flag2==1):
                    if((temp >27 or 50.00 > gas_mesurement or  gas_mesurement  > 200.00 or humid > 80 ) or flag2==1):
                        GPIO.output(fan,1)
                        sim800l.send_sms(not_num,"the fan is turned on due to: temp:{0}\n humid:{1}\n gas:{2}\n flag is {3}".format(temp,humid,gas_mesurement,flag2))
                        prev_time1 = time.time()
                        print("aho")
                    else:
                        GPIO.output(fan,0) 
                    flag2=0
                if((time.time()- prev_time2 > 120) or flag1==1):
                    if((moist > 200.00) or flag1==1):
                        GPIO.output(water_pump,1)
                        sim800l.send_sms(not_num,"the pump is turned on due to moist:{0}\n flag is {1}".format(moist,flag1))
                        prev_time2 = time.time()
                        print("aho2")
                    else:
                        GPIO.output(water_pump,0)
                    flag1=0
                    #GSM________________________________________________
                for i in range(count,count+1):
                    _sms=sim800l.read_sms(i)
                    time.sleep(0.5)
                    if(_sms != None):
                        if(_sms[3][0] ==  'p' and _sms[3][1] ==  '<'):
                           flag1 = 1
                           print("flag1")
                            
                        elif(_sms[3][0] ==  'f' and _sms[3][1] ==  '<'):
                            flag2 = 1
                            print("flag2")
                        #change number
                        elif(_sms[3][0] ==  'w' and _sms[3][1] ==  '<' and _sms[3][15] is int and _sms[3][2] == '0'):
                             not_num = _sms[3][2:16]
                             sim800l.send_sms(not_num,f"The default number has been changed to: {not_num}\n")
                             print("default num: ",not_num)
                        list_representing_all_IDs_beenRead_by_gsm.append(i)
                        count += 1
                       #camera_____________________________________________
                        '''elif(_sms[3][0] ==  'c' and _sms[3][1] ==  '<'):
                            name_count=name_count+1
                            camera.start_recording(path+name+str(name_count)+ext)
                            print("Camera on")
                            camera.wait_recording(10)
                            camera.stop_recording()
                            print("camera off")
                            send_mail()         
                            remove_file()
                        '''
                        
                    
                
                            
            #database.child("DB object name")
            res = {"Moisture": moist, 
                   "Tempreture": temp, 
                   "Humidity": humid, 
                   "Brightness": Brightness,
                   "AirQuality": gas_mesurement,
                   "TimeStamp": TimeStamp}
            database.push(res)
            
            
            
except KeyboardInterrupt:
      GPIO.cleanup()
      print('GPIO is cleaned up')



while True:
    time.sleep(.2)