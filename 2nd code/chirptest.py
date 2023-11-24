import chirp
import time

# These values needs to be calibrated for the percentage to work!
# The highest and lowest value the individual sensor outputs.


# Initialize the sensor.
chirp = chirp.Chirp(address=0x20,\
                    read_moist=True,\
                    read_temp=True,\
                    read_light=True,\
                    temp_scale='celsius')

try:
    print('Moisture  | Temp   | Brightness')
    print('-' * 31)
    while True:
        # Trigger the sensors and take measurements.
        chirp.trigger()
        output = '{:d} {:4.1f}% | {:3.1f}°C | {:d}'
        output = output.format(chirp.moist,chirp.moist,\
                               chirp.temp, chirp.light)
        print(output)
        time.sleep(1)
except KeyboardInterrupt:
    print('\nCtrl-C Pressed! Exiting.\n')
finally:
    print('Bye!')