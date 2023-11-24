import smbus
import time
bus = smbus.SMBus(1)
time.sleep(30)
                
#def read_2bytes(self,adrr,reg):   #for requesting values before reading       
'''def read_2bytes(adrr,reg):
        time.sleep(9)
        bus.write_byte(adrr,reg)
        time.sleep(9)
        measurement = bus.read_word_data(addr,reg) #arduino read it on two block of codes using wire.read() which read 1 byte at a time
        measurement = ( measurement >> 8) + (( measurement & 0xFF) << 8)
        return measurement
'''         


while 1:
    time.sleep(9)
    bus.write_byte(20,00)
    time.sleep(9)
    measurement = bus.read_word_data(0x20,0x00) #arduino read it on two block of codes using wire.read() which read 1 byte at a time
    measurement = ( measurement >> 8) + (( measurement & 0xFF) << 8)
    print(measurement)
    time.sleep(9)
    