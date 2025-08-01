m machine import Pin

beeper = Pin(5, Pin.OUT) #Ο βομβητής συνδέεται στο pin ΙΟ5

def beep(freq = 500, dur = .5): #Default values
    #Υπολογισμοί
    period = 1.0 / freq #Περίοδος
    half_per = int((period / 2) * 1000000) #Ημιπερίοδος
    times = int(dur / period) #Αριθμός κύκλων
    for i in range(times):
        beeper.value(1)
        time.sleep_us(half_per)
        beeper.value(0)
        time.sleep_us(half_per)

beep() #Θα παραχθεί τόνος 500Hz για 0,5sec
beep(1000, .5) #1000Hz
beep(2000, .5) #2000Hz

for i in range(200, 4001, 10): #Σταδιακό ανέβασμα από 200 - 4000
    beep(i, .003)
for i in range(4000, 195, -10): #Σταδιακό κατέβασμα από 4000 - 200
    beep(i, .003)