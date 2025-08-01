import machine, time
i2c = machine.I2C(0, sda = machine.Pin(21), scl = machine.Pin(22), freq = 400000)
#Ή εναλλακτικά
#i2c = machine.SoftI2C(sda=machine.Pin(21), scl=machine.Pin(22))
addr = i2c.scan()
#Εμφάνισε διευθύνσεις όλων των συσκευών του διαύλου για λόγους Debuging
print ('[{}]'.format(', '.join(hex(x) for x in addr))) #Εμφανίζει τις διαθέσιμες διευθύνσεις I2C. Σε εμάς είναι η 0x76

from bmp280 import *
bmp = BMP280(i2c)

while True:
    bmp.force_measure()
    print("Θερμοκρασία: " + str(bmp.temperature))
    print("Πίεση: " + str(bmp.pressure / 100) + "\n")
    time.sleep(5)