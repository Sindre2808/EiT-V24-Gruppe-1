# # main.py -- put your code here!



# import time







# print("Starting soil sensor test...")

# while True:
#     measurement = moist_sensor(ADC_PIN)
#     print("Measurement: " + str(measurement))

import socket
import time

from machine import ADC, Pin
from network import LTE

UDP_IP = "172.16.15.14"
UDP_PORT = 1234

ADC_PIN = "P15" 


def moist_sensor(pin):
    time.sleep(2) # Let the program sleep for X amount of seconds before continue to execute
    print("")
    adc = ADC()
    apin = adc.channel(pin=pin, attn=ADC.ATTN_11DB)
    value = apin.value()
    moisture = ((value / 4096) * 100)
    print('Moisture: ' + str(moisture))
    return moisture

lte = LTE()
#some carriers have special requirements, check print(lte.send_at_cmd("AT+SQNCTM=?")) to see if your carrier is listed.
#when using verizon, use
#lte.init(carrier=verizon)
#when usint AT&T use,
#lte.init(carrier=at&t)

#some carriers do not require an APN
#also, check the band settings with your carrier
lte.attach(band=20, apn="mda.lab5e")
print("attaching..",end='')
while not lte.isattached():
    time.sleep(0.25)

    print('.',end='')
    print(lte.send_at_cmd('AT!="fsm"'))         # get the System FSM
print("attached!")

lte.connect()
print("connecting [##",end='')
while not lte.isconnected():
    time.sleep(0.25)
    print('#',end='')
    #print(lte.send_at_cmd('AT!="showphy"'))
    print(lte.send_at_cmd('AT!="fsm"'))
print("] connected!")


sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP

print("attempting to send 10 measurements")
for i in range(10):
    print("measuring value nr", i + 1)
    message = str(moist_sensor(ADC_PIN))
    print("sending measurment nr: ", i + 1, "value: ", message)

    
    sock.sendto(bytes(message, "utf-8"), (UDP_IP, UDP_PORT))
    time.sleep(1)


print("disconnecting..",end='')
#now we can safely machine.deepsleep()
lte.deinit() #disconnect 
print("LTE connection status:" , lte.isconnected())