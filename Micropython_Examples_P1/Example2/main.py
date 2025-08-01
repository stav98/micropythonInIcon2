import time, dht
from machine import Pin

sensor = dht.DHT11(Pin(33))

while True:
    sensor.measure() 
    print("Θερμοκρασία:", sensor.temperature())
    print("Σχετ. Υγρασία:", sensor.humidity())
    time.sleep(1)