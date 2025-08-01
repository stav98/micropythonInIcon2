import time
from machine import Pin

Relay1 = Pin(16, Pin.OUT)
while True:
    Relay1.value(True)
    time.sleep_ms(1000)
    Relay1.value(False)
    time.sleep_ms(1000)