import time
from machine import Pin

PIR = Pin(4, Pin.IN, Pin.PULL_UP) #PULL_UP ώστε αν κοπεί το καλώδιο του PIR να χτυπάει πάντα
BEEPER = Pin(5, Pin.OUT) #Ο ενσωματωμένος βομβητής της πλακέτας συνδέεται στο pin ΙΟ5
LED = Pin(26, Pin.OUT) #Το LED συνδέεται στο pin ΙΟ26

# Η συνάρτηση παράγει ένα τόνο συχνότητας freq και διάρκειας dur
def tone(freq = 500, dur = .5): #Προκαθορισμένες τιμές
    #Υπολογισμοί
    period = 1.0 / freq #Περίοδος
    half_per = int((period / 2) * 1000000) #Ημιπερίοδος
    times = int(dur / period) #Αριθμός κύκλων
    for i in range(times):
        BEEPER.value(1) #Beeper ενεργό
        time.sleep_us(half_per) #Περίμενε τον χρόνο της ημιπεριόδου
        BEEPER.value(0) #Beeper ανενεργό
        time.sleep_us(half_per) #Περίμενε τον χρόνο της ημιπεριόδου

# Η συνάρτηση σαρώνει τις συχνότητες από 500Hz έως 5KHz για να ακουστεί ήχος συναγερμού
def alarm():
    for i in range(500, 5001, 20): #Σταδιακό ανέβασμα από 200 - 5000
        tone(i, .001) #Διάρκεια του κάθε τόνου 1msec

LED.value(0) #Αρχικά στο ξεκίνημα το LED είναι σβηστό
t1 = time.ticks_ms() #Κράτησε τον τρέχοντα χρόνο του χρονιστή σε msecs

# Η συνάρτηση αναβοσβήνει ασύγχρονα το λευκό LED με περίοδο 1sec 
def blink(en):
    global led_state, t1
    if en: #Αν είναι ενεργοποιημένο
        if time.ticks_ms() - t1 > 500: # Πέρασε ο χρονιστής το 0,5 sec σε σχέση με πριν; 
            t1 = time.ticks_ms() # Αν ναι ξανακράτα τον νέο χρόνο
            if not LED.value(): #Αν το LED είναι σβηστό
                LED.value(1) #Αναψέ το
            else: #Διαφορετικά
                LED.value(0) #Σβήστο
    else: #Δεν είναι ενεργοποιημένο
        LED.value(0) #Σβήσε το LED
        
# Κυρίως πρόγραμμα
# Το PIR βγάζει ψηφιακή έξοδο και αν ανιχνεύσει κίνηση παραμένη σε λογικό '1' για 2 με 3 sec
while(True): # Για πάντα
    s = PIR.value() # Διάβασε τιμή PIR να δεις αν υπάρχει κίνηση. 
    #print(">", s) # Debug
    if s: # Αν είναι 1 (True)
        alarm() # Ήχησε συναγερμό
        blink(True) # Ενεργοποίησε αναβόσβημα του LED
    else: # Διαφορετικά δεν υπάρχει κίνηση
        blink(False) # Σταμάτησε το αναβόσβημα του LED
        time.sleep(.5) # Περίμενε μισό δευτερόλεπτο και ξαναέλεγξε το PIR