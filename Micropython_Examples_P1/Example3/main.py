import machine, neopixel

np = neopixel.NeoPixel(machine.Pin(25), 5) #IO25, 5 x RGB Leds
#         R , G , B
np[0] = (255, 0, 0) #Κόκκινο 100%
np[1] = (125, 204, 223)
np[2] = (120, 153, 23)
np[3] = (255, 0, 153)
np[4] = (0, 0, 64) #Μπλε 25%
np.write()