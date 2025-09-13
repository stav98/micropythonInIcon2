import machine, time, neopixel

#Ορισμοί
threshold = 200 # Threshold to be adjusted
Debounce = 50 #msec

#Στιγμιότυπο RGB Leds
rgb = neopixel.NeoPixel(machine.Pin(25), 5) #IO25, 5 x RGB Leds

#Ορισμός ακροδεκτών κουμπιών αφής
t_pin1 = machine.TouchPad(machine.Pin(12)) #1ο κουμπί αφής
t_pin2 = machine.TouchPad(machine.Pin(13)) #2ο κουμπί αφής

#Ορισμός ακροδέκτη Beeper
beeper = machine.Pin(5, machine.Pin.OUT) #Ο βομβητής συνδέεται στο pin ΙΟ5
#Συνάρτηση παραγωγής τόνου συχνότητας freq σε Hz και διάρκειας dur σε msecs
def beep(freq = 500, dur = 500): #Προκαθορισμένο 500Hz, 500msec
    #Υπολογισμοί
    period = 1.0 / freq #Περίοδος
    half_per = int((period / 2) * 1000000) #Ημιπερίοδος σε μsecs
    times = int(dur / 1000 / period) #Αριθμός κύκλων
    for i in range(times):
        beeper.value(1)
        time.sleep_us(half_per)
        beeper.value(0)
        time.sleep_us(half_per)

#----- Ορισμός κλάσης ελέγχου κουμπιών αφής (Μόνο απλό κλικ) ------------------------------------------
class Touch:
    #Κατασκευαστής
    def __init__(self, pin):
        self.pin = pin  #Το GPIO του κουμπιού αφής
        self.validclick = False #Έγκυρο πάτημα
        self.timer = 0  #Ο timer που κρατάει τα ticks σε msec
        self.downtime = 0 #Πόσο χρόνο είναι πατημένο (Δάχτυλο πάνω στο κουμπί αφής)

    #Συμβάν απλό κλικ
    def onClick(self):
        self()

    #Καλείται περιδικά και ελέγχει το κάθε κουμπί
    def checkButton(self):
        self.timer = time.ticks_ms() #Κράτησε τον χρόνο συστήματος
        cVal = self.pin.read() #Διάβασε τιμή του αισθητήρα touch
        state = False #Δεν πατήθηκε
        if cVal < threshold: #Αν είναι κάτω από το κατώφλι (Δάχτυλο πάνω στην νησίδα)
            state = True #Πατήθηκε το κουμπί
        #------ Πατημένο ---------------------------------------------------------------------------------
        #Πατήθηκε τώρα για πρώτη φορά και ο χρόνος δεν μετράει
        if state and self.downtime == 0:
            self.downtime = self.timer #Άρχισε να μετράς τον χρόνο που είναι πατημένο - downtime
        #Παραμένει πατημένο και έλεγξε αν πέρασε ο χρόνος debounce και δεν έχει ενεργοποιηθεί valid click
        elif state and not self.validclick and (self.timer - self.downtime) > Debounce:
            self.validclick = True #Να μην ξαναμπείς εδώ
            self.onClick() #Κάλεσε συνάρτηση εξυπηρέτησης
        #------ Ελεύθερο ---------------------------------------------------------------------------------
        #Αλλιώς αν ήταν πατημένο και τώρα το άφησε 
        elif not state:
            self.downtime = 0 #Επαναφορά
            self.validclick = False #Επαναφορά για την επόμενη φορά
#----- Τέλος ορισμού κλάσης ------------------------------------------------------------------------------

#----- Συναρτήσεις εξυπηρέτησης συμβάντων ----------------------------------------------------------------
def key1_click(): #Άναψε
    print("Led is ON")
    #--------- R ,  G ,  B
    rgb[4] = (255, 255, 255) #Τιμές από 0 (σβηστό) έως 255 (μέγιστη ένταση)
    rgb.write()
    beep(2000, 50)

def key2_click(): #Σβήσε
    print("Led is OFF")
    rgb[4] = (0, 0, 0)
    rgb.write()
    beep(400, 50)

#===== Κυρίως πρόγραμμα ==================================================================================
#----- Δημιουργία στιγμιοτύπων και ορισμός συναρτήσεων εξυπηρέτησης --------------------------------------
ts1 = Touch(t_pin1)
ts1.onClick = key1_click

ts2 = Touch(t_pin2)
ts2.onClick = key2_click

print("\nESP32 Touch Buttons & RGB Leds Demo")

#----- Για πάντα -----------------------------------------------------------------------------------------
while True:
    ts1.checkButton() #Έλεγχος 1ου κουμπιού
    ts2.checkButton() #Έλεγχος 2ου κουμπιού
    time.sleep_ms(5) #Περίμενε 5 - 10msec
