from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from ezFBfont import ezFBfont
import gc

import my_unifont_15_1_05 as font1 #Εισαγωγή μεταφρασμένης γραμματοσειράς
import my_b10 as font2

i2c = I2C(0, sda = Pin(21), scl = Pin(22), freq = 400000)
display = SSD1306_I2C( width=128, height=64, i2c=i2c, addr=0x3c, external_vcc=False )
display.fill(0) #Καθαρίζει οθόνη

#Δημιουργία στιγμιοτύπου
font = ezFBfont(display, font1,
                halign='center',
                valign='top',
                hgap=1,
                verbose=True)

font1 = ezFBfont(display, font2,
                halign='center',
                valign='top',
                hgap=1,
                verbose=True)

font.write("Καλημέρα\n", 63, 0) #Εγγραφή στο Framebuffer
font1.write("Κόσμε\n", 63, 31)
display.text("Test", 90, 56)
display.show() #Παρουσίασε στην οθόνη
print(gc.mem_alloc())
print(gc.mem_free())
gc.collect()
print(gc.mem_alloc())
print(gc.mem_free())