import machine, neopixel
import time

np = neopixel.NeoPixel(machine.Pin(25), 5) #IO25, 5 x RGB Leds

def blank():
    np[0] = np[1] = np[2] = np[3] = np[4] = (0, 0, 0)
    np.write()

def fade(R = 0, G = 0, B = 0):
    #Fade in
    for i in range(0, 256, 5):
        r = i * R; g = i * G; b = i * B
        for j in range(5):
            np[j] = (r, g, b)
        np.write()
        time.sleep_ms(50)
    #Fade out
    for i in range(255, -1, -5):
        r = i * R; g = i * G; b = i * B
        for j in range(5):
            np[j] = (r, g, b)
        np.write()
        time.sleep_ms(50)

def kit(color, times):
    for k in range(times):
        for i in range(5):
            np[0] = np[1] = np[2] = np[3] = np[4] = (0, 0, 0)
            np[i] = color
            np.write()
            time.sleep_ms(100)
        for i in range(4, -1, -1):
            np[0] = np[1] = np[2] = np[3] = np[4] = (0, 0, 0)
            np[i] = color
            np.write()
            time.sleep_ms(100)

while(True):
    fade(1, 0, 0)
    fade(0, 1, 0)
    fade(0, 0, 1)
    kit((0, 255, 128), 5)
    kit((255, 0, 128), 5)
    kit((255, 0, 0), 5)
    blank()
    time.sleep(1)