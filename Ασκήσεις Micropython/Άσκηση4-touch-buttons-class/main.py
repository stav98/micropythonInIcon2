import machine, time
#---- Ορισμοί ---------------------------------------------------------------------
threshold = 200 # Threshold to be adjusted
Debounce = 50 #msec
DblClickDelay = 300 #msec
LongPressDelay = 1000 #msec
t_pin1 = machine.TouchPad(machine.Pin(12)) #1ο κουμπί αφής
t_pin2 = machine.TouchPad(machine.Pin(13)) #2ο κουμπί αφής

#----- Ορισμός κλάσης -------------------------------------------------------------
class Touch:
    #Κατασκευαστής
    def __init__(self, pin):
        self.pin = pin
        self.laststate = True
        self.timer = 0
        self.downtime = -1
        self.uptime = -1
        self.ignoreUP = False
        self.singleClickOK = False
        self.dblClickWaiting = False
        self.dblClickOnNextUp = False
        self.longPressHappened = False 

    #Συμβάντα
    #Απλό κλικ
    def onClick(self):
        self()

    #Διπλό κλικ
    def onDblClick(self):
        self()

    #Παρατεταμένο κλικ
    def onLongClick(self):
        self()
    
    #Καλείται περιδικά και ελέγχει το κάθε κουμπί
    def checkButton(self):
        resultEvent = 0
        self.timer = time.ticks_ms() #Κράτησε τον χρόνο συστήματος
        cVal = self.pin.read() #Διάβασε τιμή του αισθητήρα touch
        state = False #Δεν πατήθηκε
        if cVal < threshold: #Αν είναι κάτω από το κατώφλι
            state = True #Πατήθηκε το κουμπί
        #------ Πατημένο ----------------------------------------------------------------------
        #Πατήθηκε τώρα και πριν δεν είχε πατηθεί και o uptime έχει ξεπεράσει τον χρόνο debounce.
        #Αρχικά θα μπει εδώ αμέσως όταν πατηθεί γιατί δεν έχει κρατηθεί ο uptime 
        if state == True and self.laststate == False and (self.timer - self.uptime) > Debounce:
            self.downtime = self.timer #Άρχισε να μετράς τον χρόνο που είναι πατημένο - downtime
            self.ignoreUP = False
            self.singleClickOK = True
            self.longPressHappened = False
            #Αν δεν έχει περάσει ο χρόνος uptime τον χρόνο double click και δεν έχει ενεργοποιηθεί το double click στην επόμενη επαναφορά
            #και περιμένει για double click. Εδώ θα μπει κατά το 2ο πάτημα
            if (self.timer - self.uptime) < DblClickDelay and self.dblClickOnNextUp == False and self.dblClickWaiting == True:
               self.dblClickOnNextUp = True #Στο άφημα να το θεωρήσει διπλό κλικ
            else: #Εδώ θα μπει στο 1ο κλικ του διπλού κλικ
               self.dblClickOnNextUp = False
            self.dblClickWaiting = False #Επαναφορά για την επόμενη φορά
        #------ Ελεύθερο ----------------------------------------------------------------------
        #Αλλιώς αν ήταν πατημένο και τώρα το άφησε και πέρασε ο downtime έχει ξεπεράσει τον χρόνο debounce 
        #Εδώ θα μπει αν κρατήθηκε πατημένο για χρόνο > debounce
        elif state == False and self.laststate == True and (self.timer - self.downtime) > Debounce:
            #Αν δεν θέλει να αγνοήσει το Up. Εδώ δεν μπαίνει κατά το άφημα του long click
            if self.ignoreUP == False:
                self.uptime = self.timer #Άρχισε να μετράς τον χρόνο που είναι πάνω - uptime χρήσιμος για double click
                if self.dblClickOnNextUp == False: #Έχει γίνει το 1ο κλικ και τώρα το άφησε
                   self.dblClickWaiting = True #Θα περιμένει για δεύτερο πάτημα
                #Εδώ έχει συμβεί διπλό κλικ. Είναι πάνω μετά από διπλό κλικ
                else:
                   resultEvent = 2 #Αποτέλεσμα διπλό κλικ
                   self.dblClickOnNextUp = False #Επαναφορά
                   self.dblClickWaiting = False
                   self.singleClickOK = False

        #Έλεγχος για μονό κλικ. Ο χρόνος του διπλού κλικ έχει λήξει
        if state == False and (self.timer - self.uptime) >= DblClickDelay and self.dblClickWaiting == True and self.dblClickOnNextUp == False and \
            self.singleClickOK == True and resultEvent != 2:
            resultEvent = 1
            self.dblClickWaiting = False

        #Έλεγχος για παρατεταμένο κλικ
        if state == True and (self.timer - self.downtime) >= LongPressDelay:
            #Πυροδότησε το παρατεταμένο πάτημα
            #Αν δεν πατήθηκε πριν παρατεταμένα
            if self.longPressHappened == False:
                resultEvent = 3
                self.ignoreUP = True #Αγνόησε το άφημα
                self.dblClickOnNextUp = False
                self.dblClickWaiting = False
                self.longPressHappened = True
        
        self.laststate = state #Κράτα την προηγούμενη κατάσταση
        #Κλήσεις ανάλογα με την ενέργεια
        if resultEvent == 1:
            self.onClick()
        if resultEvent == 2:
            self.onDblClick()
        if resultEvent == 3:
            self.onLongClick()
#----- Τέλος ορισμού κλάσης --------------------------------------------------------------

#----- Συναρτήσεις εξυπηρέτησης συμβάντων ------------------------------------------------
def key1_click():
    print("key1 Click")

def key2_click():
    print("key2 Click")

def key1_dblclick():
    print("key1 Double Click")

def key2_dblclick():
    print("key2 Double Click")

def key1_longclick():
    print("key1 Long Click")

def key2_longclick():
    print("key2 Long Click")
#----- Τέλος συναρτήσεων εξυπηρέτησης συμβάντων -------------------------------------------

#===== Κυρίως πρόγραμμα ===================================================================
#----- Δημιουργία στιγμιοτύπων και ορισμός συναρτήσεων εξυπηρέτησης -----------------------
ts1 = Touch(t_pin1)
ts1.onClick = key1_click
ts1.onDblClick = key1_dblclick
ts1.onLongClick = key1_longclick

ts2 = Touch(t_pin2)
ts2.onClick = key2_click
ts2.onDblClick = key2_dblclick
ts2.onLongClick = key2_longclick

print("\nESP32 Touch Demo")

#----- Για πάντα ---------------------------------------------------------------------------
while True:
    ts1.checkButton() #Έλεγχος 1ου κουμπιού
    ts2.checkButton() #Έλεγχος 2ου κουμπιού
    time.sleep_ms(10) #Περίμενε 5 - 10msec