import time
from machine import Pin

beeper = Pin(5, Pin.OUT) #Ο βομβητής συνδέεται στο pin ΙΟ5

def beep():
    for i in range(200):
        beeper.value(1)
        time.sleep_us(1000)
        beeper.value(0)
        time.sleep_us(1000)

beep()