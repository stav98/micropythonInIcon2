import time
from machine import Pin

PIR = Pin(4, Pin.IN, Pin.PULL_UP) #PULL_UP ώστε αν κοπεί το καλώδιο του PIR να χτυπάει πάντα
BEEPER = Pin(5, Pin.OUT) #Ο ενσωματωμένος βομβητής της πλακέτας συνδέεται στο pin ΙΟ5
WLED = Pin(26, Pin.OUT) #Το λευκό LED συνδέεται στο pin ΙΟ26
RLED = Pin(32, Pin.OUT) #Το κόκκινο LED συνδέεται στο pin ΙΟ32
BUTTON = Pin(34, Pin.IN, Pin.PULL_UP) #PULL_UP

Alarm_EN = False #Flag για ενεργοποίηση συναγερμού

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

# Ενέργεια αν πατηθεί το button
def onClick():
    global Alarm_EN
    if not Alarm_EN:
        Alarm_EN = True
        tone(1000, .2)
    else:
        Alarm_EN = False
        tone(500, .1)

Debounce = 30 #msec Χρόνος αναπήδησης επαφής
validclick = False
timer = 0
downtime = 0

# Καλείται συνέχεια από το κυρίως πρόγραμμα και ελέγχει αν πατήθηκε το button
def chkButton():
    global validclick, timer, downtime
    timer = time.ticks_ms() #Κράτησε τον χρόνο συστήματος
    state = False #Δεν πατήθηκε
    if not BUTTON.value(): #if BUTTON.value() == 0
        state = True #Πατήθηκε το κουμπί
    #------ Πατημένο ---------------------------------------------------------------------------------
    #Πατήθηκε τώρα για πρώτη φορά και ο χρόνος δεν μετράει
    if state and downtime == 0:
        downtime = timer #Άρχισε να μετράς τον χρόνο που είναι πατημένο - downtime
    #Παραμένει πατημένο και έλεγξε αν πέρασε ο χρόνος debounce και δεν έχει ενεργοποιηθεί valid click
    elif state and not validclick and (timer - downtime) > Debounce:
        validclick = True #Να μην ξαναμπείς εδώ
        onClick() #Κάλεσε συνάρτηση εξυπηρέτησης
    #------ Ελεύθερο ---------------------------------------------------------------------------------
    #Αλλιώς αν ήταν πατημένο και τώρα το άφησε 
    elif not state:
        downtime = 0 #Επαναφορά
        validclick = False #Επαναφορά για την επόμενη φορά
        
#Κλάση για αναβόσβημα των LED
class Blink:
    def __init__(self, Led, Dur):
        self.Led = Led #IO pin του LED
        self.Dur = Dur #Διάρκεια ημιπεριόδου
        self.t = time.ticks_ms() #Χρονιστής
        self.en = False #Ενεργοποιημένο
    
    def blink(self):
        if self.en: #Αν είναι ενεργοποιημένο
            if time.ticks_ms() - self.t > self.Dur: # Πέρασε ο χρονιστής το 0,5 sec σε σχέση με πριν; 
                self.t = time.ticks_ms() # Αν ναι ξανακράτα τον νέο χρόνο
                if not self.Led.value(): #Αν το LED είναι σβηστό
                    self.Led.value(1) #Αναψέ το
                else: #Διαφορετικά
                    self.Led.value(0) #Σβήστο
        else: #Δεν είναι ενεργοποιημένο
            self.Led.value(0) #Σβήσε το LED
    
#Στιγμιότυπα για τα 2 LED
blinkRed = Blink(RLED, 100) #Κόκκινο με περίοδο 200msec
blinkRed.en = False #Αρχικά δεν αναβοσβήνει
blinkWhite = Blink(WLED, 500) #Λευκό με περίοδο 1sec
blinkWhite.en = False #Αρχικά σβηστό
      
# Κυρίως πρόγραμμα - εκτελείται συνέχεια
# Το PIR βγάζει ψηφιακή έξοδο και αν ανιχνεύσει κίνηση παραμένη σε λογικό '1' για 2 με 3 sec
while(True): # Για πάντα
    chkButton() #Έλεγχος αν πατήθηκε το Button
    blinkRed.blink() #Κάλεσε μέθοδο για αναβόσβημα του κόκκινου
    blinkWhite.blink() #Κάλεσε μέθοδο για αναβόσβημα του λευκού
    if Alarm_EN: #Αν έχει ενεργοποιηθεί ο συναγερμός
        blinkRed.en = True #Να αναβοσβήνει το κόκκινο LED
    else: #Διαφορετικά 
        blinkRed.en = False #Nα σταματήσει τις αναλαμπές
    s = PIR.value() # Διάβασε τιμή PIR να δεις αν υπάρχει κίνηση. 
    if s and Alarm_EN: # Αν είναι 1 (True) ανιχνεύθηκε κίνηση και έχει ενεργοποιηθεί 
        alarm() # Ήχησε συναγερμό
        blinkWhite.en = True # Ενεργοποίησε αναβόσβημα του λευκού LED
    else: # Διαφορετικά δεν υπάρχει κίνηση ή είναι απενεργοποιημένο
        blinkWhite.en = False # Σταμάτησε το αναβόσβημα του λευκού LED
        time.sleep(.02) # Περίμενε 20msec και ξαναέλεγξε το PIR