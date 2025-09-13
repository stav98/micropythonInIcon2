# Πρόγραμμα το οποίο παρουσιάζει μετρήσεις Θερμοκρασίας και υγρασίας από DHT11 
# και ατμ. πίεσης και θερμοκρασίας από το BMP280 στην οθόνη OLED
import machine, time, dht, math
i2c = machine.I2C(0, sda = machine.Pin(21), scl = machine.Pin(22), freq = 400000)
#Ή εναλλακτικά
#i2c = machine.SoftI2C(sda=machine.Pin(21), scl=machine.Pin(22))
from ssd1306 import SSD1306_I2C #Ο ελεγκτής της οθόνης OLED
sensor = dht.DHT11(machine.Pin(33)) #Ο αισθητήρας DHT11
from bmp280 import *
bmp = BMP280(i2c) #Στιγμιότυπο του BMP280
#Στιγμιότυπο της οθόνης.
display = SSD1306_I2C(width=128, height=64, i2c=i2c, addr=0x3c, external_vcc=False)
display.fill(0) #Καθαρίζει οθόνη

#Δημιούργησε διπλό περίγραμμα
display.rect(0, 0, 127, 63, 1, 0) #x, y, width, heigh, color=0/1, fill=0/1
display.rect(2, 2, 123, 59, 1, 0) #x, y, width, heigh, color=0/1, fill=0/1

#Δημιούργησε ετικέτες
display.rect(3, 2, 121, 14, 1, 1) #x, y, width, heigh, color=0/1, fill=0/1
display.text('Weather Station', 3, 5, 0) #Θέση x, y, color 1/0
display.text("Press: ", 5, 20, 1)
display.text("hpa", 100, 20, 1)
display.text("Temper1 : ", 5, 30, 1)
display.ellipse(113, 31, 1, 1, 1)
display.text("C", 115, 30, 1)
display.text("Temper2 : ", 5, 40, 1)
display.ellipse(106, 41, 1, 1, 1)
display.text("C", 108, 40, 1)
display.text("Humidity: ", 5, 50, 1)
display.text("%", 105, 50, 1)
display.show() #Παρουσίασε στην οθόνη

#Για πάντα
while True:
    bmp.force_measure() #Διάβασε τιμές από BMP280
    display.rect(52, 19, 48, 9, 0, True) #Σβήσε παλιά τιμή ατμ. πίεσης
    display.text(str(round((bmp.pressure / 100), 1)), 52, 20, 1) #Εμφάνισε νέα τιμή ατμ. πίεσης
    display.rect(77, 29, 34, 9, 0, True) #Σβήσε παλιά τιμή θερμοκρασίας BMP
    display.text(str(round(bmp.temperature, 1)), 78, 30, 1) #Εμφάνισε νέα τιμή Θερμοκρασίας BMP
    print("Θερμοκρασία BMP: " + str(round(bmp.temperature, 1))) #Εμφάνισε σε τερματικό
    print("Πίεση: " + str(round((bmp.pressure / 100), 1))) #Εμφάνισε σε τερματικό
    
    sensor.measure() #Διάβασε τιμές από DHT11
    display.rect(80, 39, 25, 9, 0, True) #Σβήσε παλιά τιμή Θερμοκρασίας DHT
    display.text("{: 3}".format(sensor.temperature()), 80, 40, 1) #Εμφάνισε νέα τιμή θερμοκρ. DHT
    display.rect(80, 49, 25, 9, 0, True) #Σβήσε παλιά τιμή σχετ, υγρασίας
    display.text("{: 3}".format(sensor.humidity()), 80, 50, 1) #Εμφάνισε νέα τιμή υγρασίας
    print("Θερμοκρασία DHT:", sensor.temperature()) #Εμφάνισε στο τερματικό 
    print("Σχετ. Υγρασία:", sensor.humidity()) #Εμφάνισε στο τερματικό
    print() #Άσε μια γραμμή κενή

    display.show() #Παρουσίασε στην οθόνη
    time.sleep(2) #Περίμενε 2 sec
