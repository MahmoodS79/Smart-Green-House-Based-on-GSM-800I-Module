
# Smart Green House Based on GSM 800I Module

### High Level Description
>The project will report any abnormal condition of the plant to the client and automatically or remotely(manually) the circuit will try to make conditions better by controlling a fan , a pump and a light bulb

### Detailed Description
>This project will initially initialize the hw components RaspberryPi, GSM module, the firebase cloud database, the analog sensors, and Pi camera inputs and outputs.

>Next the code will enter a loop to take measurements every 20 sec of the plant condition, through moisture sensor, gas sensor, light sensor, and temperature humidity sensor. Then stores all measurements in a file with the time and date stamp.

>Pi must detect any unusual condition of any specified measurements through conditional codes, if humidity or gas wasn't good a fan is to blow air in the Mackett. If moisture measurements weren’t good a pump will pump water into the soil, if light wasn't good a certain degree of light is to be powered and increase it in ramp if no progress in the measurements.

>GSM module will get certain CMDs from the PI to send messages or make a call. This module can Rx CMDs from a certain mobile number to operate a certain action like turn pump on or fan on or light on as user specify in the MSG with the specified CMDs in the code.

>Pi will record the plant on unusual measurements and report the record and all measurements to a firebase database where a mobile application shows the report as a dashboard.


## Installation

>First Pi must be attached to pure 5v power supply and GSM module will be given 4.7 rechargeable battery. The pump and the fan will be given a 12v as input to transistor(switch). All the analog sensors must be provided with another 5v power supply.  
* Analog Sensors are input to ADC:   
>>Gas sensor --> ch0  
moist sensor --> ch1  
light sensor --> ch2  
* DHT11 digital Sensor :   
>>analog output --> pin # 15 gpio 22  
* GSM module :   
>>TX pin---> pin 10 gpio 15  
(the head of the 1N4148 diode must be connected to the TX pin of the GSM and the tail to a resistor of 10k ohms and 3.3v in the PI )   
>>RX pin --->  pin 8 gpio 14  
* BC546 Transistor module :   
>>base pin of the fan     ---> pin 37 gpio 26    
>>base pin of he pump    --->  pin 35 gpio 19     

here are some schematics: 



![schematics for project_Page_1](https://github.com/MahmoodS79/Smart-Green-House-Based-on-GSM-800I-Module/assets/87457802/8b4143c7-6b67-4fa5-bb0e-e0cc1bd3640e)
![schematics for project_Page_2](https://github.com/MahmoodS79/Smart-Green-House-Based-on-GSM-800I-Module/assets/87457802/335d4d79-5fb1-4a57-a5d2-a089e91ab93f)
![Pages from Binder4 pdf](https://github.com/MahmoodS79/Smart-Green-House-Based-on-GSM-800I-Module/assets/87457802/5b0e57ac-c2c7-46cc-ba41-a512761895d7)
![pic](https://github.com/MahmoodS79/Smart-Green-House-Based-on-GSM-800I-Module/assets/87457802/412d7b2b-5d15-468a-b153-905b34d37f22)

>Secondly put all the circuit into the Mackett, moist into the soil, gas near the soil, and temp near the soil, also the light sensor must be close to the soil.

>Third the pump must be put into the soil connected to a tank and the fan will be put on the Mackett edges.

>fourth step just clone the code folder into PI 
and run  **main_file_to_run.py** file on Raspberry pi remotely using putty  
>>the PI settings:  
ip = raspberrypi.local  
port = 22  
username = raspberrypi  
password = raspberry   
if the settings of the PI weren't changed   
**after that the project will operate properly if the PI was permanently provided with WIFI.**

    
## Usage/Examples
using bash you can run the code
```bash
[user@client user/home/Desktop]$git clone https://github.com/MahmoodS79/Smart-Green-House-Based-on-GSM-800I-Module/tree/master/code

[user@client user/home/Desktop]$./code/main\ file\ to\ run.py
or
[user@client user/home/Desktop]$ python code/main\ file\ to\ run.py
```

