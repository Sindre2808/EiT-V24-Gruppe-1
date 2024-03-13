# get the raw data from a DHT11/DHT22/AM2302 sensor
from time import sleep_ms

import adafruit_dht
from machine import Pin
from pycom import pulses_get

# pin = Pin("P23", mode=Pin.OPEN_DRAIN)
# pin(0)
# sleep_ms(20)
# pin(1)
# data = pulses_get(pin, 100)
# print("Data:" , data , "=======================================")

sensor = adafruit_dht.DHT11(Pin(23))

print("Temp:" , sensor.temperature(), "+++++++++")
print("humidity:",  sensor.humidity(), "=========")
