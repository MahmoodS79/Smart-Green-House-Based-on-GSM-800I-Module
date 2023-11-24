#*************constants*******************
#The load resistance on the board
RLOAD = 10.0
#Calibration resistance at atmospheric CO2 level
RZERO = 76.63
#Parameters for calculating ppm of CO2 from sensor resistance
PARA = 116.6020682
PARB = 2.769034857

#Parameters to model temperature and humidity dependence
CORA = 0.00035
CORB = 0.02718
CORC = 1.39538
CORD = 0.0018
CORE = -0.003333333
CORF = -0.001923077
CORG = 1.130128205

#Atmospheric CO2 level for calibration purposes
ATMOCO2 = 397.13

#*****************************************class**************************************************
class mq135:
    def __init__(self,analog_value):
        self.anal=analog_value
    
    def getCorrectionFactor(self,t, h):
        '''Linearization of the temperature dependency curve under and above 20 degree C
            below 20degC: fact = a * t * t - b * t - (h - 33) * d
            above 20degC: fact = a * t + b * h + c
            this assumes a linear dependency on humidity
        '''
        if(t < 20):
            return CORA * t * t - CORB * t + CORC - (h-33.)*CORD
        else:
            return CORE * t + CORF * h + CORG
            

    def getResistance(self):
        #Get the resistance of the sensor, ie. the measurement value
        return ((1023/self.anal) - 1)*RLOAD


    def getCorrectedResistance(self,t, h):
        #The corrected sensor resistance kOhm
        return getResistance()/getCorrectionFactor(t, h)


    def get_ppm(self):
        # Get the ppm of CO2 sensed (assuming only CO2 in the air)
        return PARA * (self.getResistance()/RZERO)**(-PARB)


    def getCorrectedPPM(self,t, h):
        return  PARA * (getCorrectedResistance(t, h)/RZERO)**(-PARB)


