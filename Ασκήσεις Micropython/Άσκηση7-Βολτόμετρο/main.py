from machine import Pin, ADC, I2C
from time import sleep
from ssd1306 import SSD1306_I2C

AVG_FACTOR = 2.0 #Συντελεστής μέσης τιμής όσο μεγαλύτερος τόσο πιο αργή μεταβολή
OFFS_COEF = .95 #Συντελεστής διόρθωσης
avg_voltage = 0

pot = ADC(Pin(4)) #4, 26, 32, 34
pot.width(ADC.WIDTH_12BIT) #Ευκρίνεια 12BIT προκαθορισμένο, 9BIT, 10BIT, 11BIT
pot.atten(ADC.ATTN_11DB) # πλήρης κλίμακα έως 3.3V

i2c = I2C(0, sda = Pin(21), scl = Pin(22), freq = 400000)
display = SSD1306_I2C( width=128, height=64, i2c=i2c, addr=0x3c, external_vcc=False )
display.fill(0) #Καθαρίζει οθόνη
#Δημιούργησε ετικέτες
display.text('* Volt Meter *', 5, 5, 1) #Θέση x, y, color 1/0
display.text("Voltage: ", 5, 35, 1)
display.text("V", 108, 35, 1)
#Δημιούργησε διπλό περίγραμμα
display.rect(0,0,127,63,1,0) #x, y, width, heigh, color=0/1, fill=0/1
display.rect(2,2,123,59,1,0) #x, y, width, heigh, color=0/1, fill=0/1
display.show() #Παρουσίασε στην οθόνη

while True:
  pot_value = pot.read()
  voltage = pot_value * (3.3 / 4096) / OFFS_COEF #12bit Στιγμιαία τιμή
  avg_voltage = (AVG_FACTOR * avg_voltage + voltage) / (AVG_FACTOR + 1) #Μέση τιμή
  print("τιμή:", pot_value, "τάση:", round(voltage, 2), "V")
  display.rect(68, 34, 40, 9, 0, True) #Σβήσε παλιά τιμή
  display.text(str(round(avg_voltage, 2)), 68, 35, 1) #Εμφάνισε νέα τιμή
  display.show() #Παρουσίασε στην οθόνη
  sleep(0.5)
