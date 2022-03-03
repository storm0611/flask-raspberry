import RPi.GPIO as GPIO
import time
from datetime import datetime

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 6
SPIMISO = 13
SPIMOSI = 19
SPICS = 26
mq7_apin = 0

#port init
def init():
         GPIO.setwarnings(False)
         GPIO.cleanup()			#clean up at the end of your script
         GPIO.setmode(GPIO.BCM)		#to specify whilch pin numbering system
         # set up the SPI interface pins
         GPIO.setup(SPIMOSI, GPIO.OUT)
         GPIO.setup(SPIMISO, GPIO.IN)
         GPIO.setup(SPICLK, GPIO.OUT)
         GPIO.setup(SPICS, GPIO.OUT)

#read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)	

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout
#main ioop
def main():
         init()

         while True:
                 Voltage=readadc(mq7_apin, SPICLK, SPIMOSI, SPIMISO, SPICS)
                 #print(Voltage)
                 VoltageOutput=(Voltage*(3.3/1024)*5.05)
                 #print(VoltageOutput)
                 Voltage=(round(VoltageOutput, 1))
                 #print(Voltage)
                 now = datetime.now()
                 dt_string = now.strftime("%d/%m/%Y %H:%M")
                 print(str(dt_string) + str(' -> ')+ str(Voltage),file=open("../readings/voltage.txt", "w"))
                 #print(str(dt_string) + str(' -> ')+ str(Voltage))#,file=open("../readings/voltage.txt", "w"))
                 time.sleep(5)

#file=open("readings/battery.txt", "w")

if __name__ =='__main__':
         try:
                  main()
                  pass
         except KeyboardInterrupt:
                  pass

GPIO.cleanup()
         
         
