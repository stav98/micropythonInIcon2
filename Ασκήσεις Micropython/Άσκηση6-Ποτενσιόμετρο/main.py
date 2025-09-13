from machine import Pin, ADC
from time import sleep

pot = ADC(Pin(4)) #4, 26, 32, 34
pot.width(ADC.WIDTH_12BIT) #Ευκρίνεια 12BIT προκαθορισμένο, 9BIT, 10BIT, 11BIT
pot.atten(ADC.ATTN_11DB) # πλήρης κλίμακα έως 3.3V

while True:
  pot_value = pot.read()
  voltage = pot_value * (3.3 / 4096) #12bit
  print("τιμή:", pot_value, "τάση:", round(voltage, 2), "V")
  sleep(0.5)