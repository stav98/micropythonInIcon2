import machine, time
i2c = machine.I2C(0, sda = machine.Pin(21), scl = machine.Pin(22), freq = 400000)
#Ή εναλλακτικά
#i2c = machine.SoftI2C(sda=machine.Pin(21), scl=machine.Pin(22))
addr = i2c.scan()
#Εμφάνισε διευθύνσεις όλων των συσκευών του διαύλου για λόγους Debuging
print ('[{}]'.format(', '.join(hex(x) for x in addr))) #Εμφανίζει τις διαθέσιμες διευθύνσεις I2C. Σε εμάς είναι η 0x76

from ssd1306 import SSD1306_I2C
#display = SSD1306_I2C(128, 64, i2c) #Δίπλα μπορώ να βάλω διεύθυνση π.χ. SSD1306_I2C(128, 64, i2c, 0x3c)
display = SSD1306_I2C( width=128, height=64, i2c=i2c, addr=0x3c, external_vcc=False )
display.text('Hello', 5, 5)  #Θέση x, y
display.text('World', 5, 15, 1) #color 1/0
display.rect(0,0,127,63,1,0) #x, y, width, heigh, color=0/1, fill=0/1
display.show()

#display.fill(0) #Καθαρίζει οθόνη
#display.show()