#python imports
import json
import socket
import time

#mycropython imports
from machine import ADC, Pin
from network import LTE

UDP_IP = "172.16.15.14"
UDP_PORT = 1234

#Data pin, can be changed to any pin that supports ADC
# On the Pycom makr, connect the ground pin to GND, VCC to 3.3V the data pin to this one
ADC_PIN = "P15" 


def moist_sensor(pin):
    time.sleep(2) # Let the program sleep for X amount of seconds before continue to execute
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

locations = [("TRONDHEIM", [63.4305, 10.3951]), ("TRONDHEIM",[63.399259, 10.454945]), ("TRONDHEIM",[63.376062, 10.499731]), \
            ("TRONDHEIM",[63.408187, 10.594553]), ("KONGSVINGER",[60.235131, 11.982647]), ("KONGSVINGER",[60.174869, 11.900502])]

print("attempting to send ", len(locations), " measurements")

for i, loc in enumerate(locations):
    print("measuring value nr", i + 1)
    message_dict = {
            "measurement": moist_sensor(ADC_PIN),
            "area": loc[0],
            "coordinates": loc[1]
        }
    message = json.dumps(message_dict)
    print("sending measurment nr: ", i + 1, "value: ", message)
    sock.sendto(bytes(message, "utf-8"), (UDP_IP, UDP_PORT))
    
    # Decide suitable time to sleep between making measurements
    # This type of soil sensors is designed to make measurements very rarely, 
    # and should sleep for longer time to avoid uneccesary corrosion
    time.sleep(1)



print("disconnecting..", end='')
lte.disconnect()
print("LTE connection status:" , lte.isconnected())
print("detaching..", end='')

lte.detach() 
print("LTE connection status:" , lte.isattached())
print("deiniting..", end='')

# "Disables LTE modem completely. This reduces the power consumption to the minimum. Call this before entering deepsleep."
lte.deinit() 
print("Did deinit work? Hopefully no error thrown")

