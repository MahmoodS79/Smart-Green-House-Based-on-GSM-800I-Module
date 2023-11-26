
### Smart Green House Based on GSM 800I Module

This project will initially initialize the hw components RaspberryPi, GSM module, the firebase cloud database, the analog sensors, and Pi camera inputs and outputs.

Next the code will enter a loop to take measurements every 20 sec of the plant condition, through moisture sensor, gas sensor, light sensor, and temperature humidity sensor. Then stores all measurements in a file with the time and date stamp.

Pi must detect any unusual condition of any specified measurements through conditional codes, if humidity or gas wasn't good a fan is to blow air in the mackett. If moisture measurements weren’t good a pump will pump water into the soil, if light wasn't good a certain degree of light is to be powered and increase it in ramp if no progress in the measurements.

GSM module will get certain CMDs from the PI to send messages or make a call. This module can Rx CMDs from a certain mobile number to operate a certain action like turn pump on or fan on or light on as user specify in the MSG with the specified CMDs in the code.

Pi will record the plant on unusual measurements and report the record and all measurements to a firebase database where a mobile application shows the report as a dashboard.




## Authors

- Marc Atef
- Fares Ali
- Omar Khaled
- Mahmood Farhat Ali
- Rawan Emad


## Installation

First Pi must be attached to pure 5v power supply and GSM module will be given 4.7 rechargeable battery. The pump and the fan will be given a 12v as input to transistor(switch). All the analog sensors must be provided with another 5v power supply.

Secondly put all the circuit into the mackett, moist into the soil, gas near the soil, temp near the soil, also the light sensor must be close to the soil.

Third the pump must be put into the soil connected to a tank and the fan will be put on the mackett edges.

Fourth step the py code must be burned or run on the PI after that the project will operate properly if the PI was permanently provided with WIFI.

    
## Usage/Examples

```python
try:
      print('Moisture,Temp,Humidtity,Brightness,AirQuality, TimeStamp')
      while True:
          '''this loop is taking measurements from all sensors it is a snapshot of the plant condition every 30sec max
          this loop will permanently provide the firebase with measurements '''

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
```

