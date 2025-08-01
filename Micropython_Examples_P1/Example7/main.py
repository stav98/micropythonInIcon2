# ------- Διεύθυνση I2C -----
I2C_Addr = 0x27 #  Η διεύθυνση μπορεί να αλλάξει στο πίσω πλακετάκι του PCF8574

# ------- Διαστάσεις LCD οθόνης ----
LCD_Dim = (16, 2)

from machine import I2C,  Pin
i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=100000)

import gc
from time import sleep
from lcd_i2c8574 import I2cLcd

lcd = I2cLcd(i2c, I2C_Addr, LCD_Dim)
gc.collect() #Συλλογή σκουπιδιών
mfree1 = gc.mem_free() #Ελεύθερη μνήμη RAM

lcd.clear() #Καθαρισμός οθόνης και τοποθέτηση cursor στην θέση 0, 0
lcd.write('Hello World', end='')
lcd.move_to(2, 1) #Τοποθέτησε cursor στην 3η στήλη, 2η γραμμή
lcd.write("Free:" + str(mfree1), end='')