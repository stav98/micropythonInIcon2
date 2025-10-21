from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from writer import Writer
import ArianaVioleta_python, FreeSerifBold_python #Μεταφρασμένες γραμματοσειρές

i2c = I2C(0, sda = Pin(21), scl = Pin(22), freq = 400000)
display = SSD1306_I2C( width=128, height=64, i2c=i2c, addr=0x3c, external_vcc=False )
display.fill(0) #Καθαρίζει οθόνη

wri1 = Writer(display, ArianaVioleta_python) #Χρήση γραμματοσειράς στο wri1
wri2 = Writer(display, FreeSerifBold_python) #Χρήση γραμματοσειράς στο wri2
wri1.set_textpos(display, 0, 0) #Αρχική θέση y, x
wri1.printstring("Hello") #Εμφάνιση κειμένου
wri2.set_textpos(display, 30, 0) #Αρχική θέση y, x
wri2.printstring("World")
display.text("Test", 90, 56) #Εμφάνιση κειμένου με τον κλασικό τρόπο στην θέση x, y
display.show() #Παρουσίασε στην οθόνη