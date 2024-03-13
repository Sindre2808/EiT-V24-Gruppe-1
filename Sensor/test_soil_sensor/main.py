
import time

from machine import ADC, Pin

ADC_PIN = "P15" #Pin("P15", mode=Pin.IN)


def moist_sensor(pin):
    time.sleep(2) # Let the program sleep for X amount of seconds before continue to execute
    print("")
    adc = ADC()
    apin = adc.channel(pin=pin, attn=ADC.ATTN_11DB)
    value = apin.value()
    moisture = ((value / 4096) * 100)
    print('Moisture: ' + str(moisture))
    return moisture
    

print("Starting soil sensor test...")

while True:
    measurement = moist_sensor(ADC_PIN)
    print("Measurement: " + str(measurement))