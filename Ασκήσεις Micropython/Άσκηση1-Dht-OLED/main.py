#Πρόγραμμα το οποίο παρουσιάζει μετρήσεις Θερμοκρασίας και υγρασίας από DHT11 στην οθόνη OLED
import machine, time, dht
i2c = machine.I2C(0, sda = machine.Pin(21), scl = machine.Pin(22), freq = 400000)
#Ή εναλλακτικά
#i2c = machine.SoftI2C(sda=machine.Pin(21), scl=machine.Pin(22))
from ssd1306 import SSD1306_I2C
sensor = dht.DHT11(machine.Pin(33))
sensor.measure() 

#display = SSD1306_I2C(128, 64, i2c) #Δίπλα μπορώ να βάλω διεύθυνση π.χ. SSD1306_I2C(128, 64, i2c, 0x3c)
display = SSD1306_I2C( width=128, height=64, i2c=i2c, addr=0x3c, external_vcc=False )
display.fill(0) #Καθαρίζει οθόνη
#Δημιούργησε ετικέτες
display.text('Hello World', 5, 5, 1) #Θέση x, y, color 1/0
display.text("Temper. : ", 5, 35, 1)
display.ellipse(106, 36, 1, 1, 1)
display.text("C", 108, 35, 1)
display.text("Humidity: ", 5, 45, 1)
display.text("%", 105, 45, 1)
#Δημιούργησε διπλό περίγραμμα
display.rect(0,0,127,63,1,0) #x, y, width, heigh, color=0/1, fill=0/1
display.rect(2,2,123,59,1,0) #x, y, width, heigh, color=0/1, fill=0/1
display.show() #Παρουσίασε στην οθόνη

#Για πάντα
while True:
    sensor.measure()
    display.rect(80, 34, 25, 9, 0, True) #Σβήσε παλιά τιμή
    display.text("{: 3}".format(sensor.temperature()), 80, 35, 1) #Εμφάνισε νέα τιμή
    display.rect(80, 44, 25, 9, 0, True) #Σβήσε παλιά τιμή
    display.text("{: 3}".format(sensor.humidity()), 80, 45, 1) #Εμφάνισε νέα τιμή
    print("Θερμοκρασία:", sensor.temperature()) #Εμφάνισε στο τερματικό
    print("Σχετ. Υγρασία:", sensor.humidity())
    display.show() #Παρουσίασε στην οθόνη
    time.sleep(2) #Περίμενε 2 sec
