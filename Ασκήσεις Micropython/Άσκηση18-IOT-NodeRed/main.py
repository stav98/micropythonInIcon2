# ===== Κυρίως πρόγραμμα εκτελείται μετά το boot.py ====
import network, gc, time, binascii, ntptime, dht
from machine import Pin, unique_id
from umqtt.simple import MQTTClient

# Ορισμοί ακροδεκτών και αισθητήρων
BUTTON1 = Pin(34, Pin.IN, Pin.PULL_UP) #PULL_UP
Relay1 = Pin(16, Pin.OUT)
sensor1 = dht.DHT11(Pin(33))

# Στοιχεία σύνδεσης στον μεσίτη MQTT
mqtt_server = '192.168.42.30' #Διεύθυνση IP ή όνομα π.χ. mqtt1.example.sch.gr
mqtt_user = 'mqttuser' #Προαιρετικά αν απαιτείται πιστοποίηση
mqtt_pass = '123456'
client_id = binascii.hexlify(unique_id()) #Το όνομα client αν θέλω να το χρησιμοποιήσω στα topics
place = "place1" #Τοποθεσία της συσκευής π.χ. bathroom, bedroom, livingroom, wc1 κλπ.
print("Ταυτότητα: %s" % (client_id.decode("utf-8"))) #Εμφάνιση ταυτότητας στο τερματικό

# Συγχρονισμός ώρας με ntp server
ntptime.host = "europe.pool.ntp.org"
ntptime.timeout = 3
ntptime.settime() # Συγχρονισμός
UTC_OFFSET = 3 # Ελλάδα +3 ώρες θερινή

# --- Ορισμός των topics ---
# Θα χρησιμοποιήσουμε για κάθε συσκευή 3 topics.
# Ένα sub στο οποίο κάνει συνδρομή η συσκευή και ακούει συνεχώς για δημοσίευση μηνυμάτων και
# δύο pub για δημοσίευση μηνυμάτων προς τον μεσίτη. Το τελευταίο (tele) είναι για αποστολή τηλεμετρίας και
# δημοσιεύει σε τακτά χρονικά διαστήματα π.χ. κάθε 1 λεπτό
topic1_sub = b'cmnd/' + place + '/POWER1' # Συνδρομή
topic1_pub = b'stat/' + place + '/POWER1' # Δημοσίευση αν γίνει αλλαγή κατάστασης
topic2_pub = b'tele/' + place + '/STATE'  # Δημοσίευση κάθε ν δευτερόλεπτα
# Ορισμός περιόδου tele
TELE = 1 # Λεπτά
TelePeriod = TELE * 60 * 1000 # secs * msecs
Resync = 3 # Ώρες. Επανασυγχρονισμός με ntp server
NTP_SYNC = Resync * 60 // TELE 

# Δημοσιεύει μήνυμα stat ώστε να ενημερώσει για την κατάσταση του διακόπτη
def stat_pub(topic, message):
    client.publish(topic, message, retain=True) # Πρέπει να είναι Retain
    print("Stat:", message) # Debug 

# Ενεργοποιεί ή απενεργοποιεί την συσκευή
def set_relay(state):
    if state:
        print("Η συσκευή ενεργοποιήθηκε") # Debug
        stat_pub(topic1_pub, b'ON')
        Relay1.value(True) # Κλείσιμο επαφής
    else:
        print("Η συσκευή απενεργοποιήθηκε") # Debug
        stat_pub(topic1_pub, b'OFF')
        Relay1.value(False) # Άνοιγμα επαφής

# Ενέργεια αν πατηθεί το button
def onClick():
    if not Relay1.value(): # Αν είναι OFF
        set_relay(True) # Να γίνει ON
    else: # Αλλιώς
        set_relay(False) # Να γίνει OFF

# Καθολικές μεταβλητές για chkButton
Debounce = 30 #msec Χρόνος αναπήδησης επαφής
validclick = False
timer = 0
downtime = 0

# Καλείται συνέχεια από το κυρίως πρόγραμμα και ελέγχει αν πατήθηκε το button
def chkButton():
    global validclick, timer, downtime
    timer = time.ticks_ms() #Κράτησε τον χρόνο συστήματος
    state = False #Δεν πατήθηκε
    if not BUTTON1.value(): #if BUTTON.value() == 0
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

# Εξυπηρέτηση δημοσιέυσεων στα topics που έγινε συνδρομή
def sub_cb(topic, msg):
    print((topic, msg)) # Debug
    if topic == topic1_sub: # Αν το topic μας αφορά π.χ. cmnd/place1/POWER1
        if msg == b'ON': # Αν το μήνυμα είναι ON
            set_relay(True) # Ενεργοποίηση συσκευής
        elif msg == b'OFF': # Αν το μήνυμα είναι OFF
            set_relay(False) # Απενεργοποίηση συσκευής

# Σύνδεση στον broker και συνδρομή στα topics
def connect_and_subscribe():
    client = MQTTClient(client_id, mqtt_server, user=mqtt_user, password=mqtt_pass)
    client.set_callback(sub_cb) # Συνάρτηση callback. Καλείται αν λάβει μήνυμα από μεσίτη
    try:
        client.connect() # Σύνδεση
        client.subscribe(topic1_sub) # Συνδρομή
        print('Συνδέθηκε στον μεσίτη MQTT %s και έγινε συνδρομή στα θέματα: %s' % (mqtt_server, topic1_sub.decode("utf-8")))
        return client
    except:
        print('Πρόβλημα στη σύνδεση')

# Διαβάζει την ημερομηνία και την ώρα συστήματος
def get_time():
    t = time.gmtime(time.time() + UTC_OFFSET * 3600)
    ts = str(t[2]) + '/' + str(t[1]) + '/' + str(t[0]) + '-' + str(t[3]) + ':' + str(t[4]) + ':' + str(t[5])
    return ts

Relay1.value(False) # Αρχικά ο διακόπτης θα είναι off

# Προσπάθεια σύνδεσης στον broker
client = connect_and_subscribe()
if client == None:
    print('Προσπάθεια επανασύνδεσης ...')
    time.sleep(5)
    machine.reset()

print('Ώρα συστήματος:', get_time()) # Debug

tele_time = 0 # Μετρητής περιόδου tele
measure_time = 0 # Μετρητής χρόνου δειγματοληψίας μετρήσεων
ntp_sync = NTP_SYNC
while True: # Για πάντα
    client.check_msg() # Έλεγξε για μήνυμα που αφορά την συνδρομή συνεχώς
    chkButton() # Έλεγξε μήπως πατήθηκε το button
    if time.ticks_ms() - measure_time > 5000: # Κάθε 5 secs
        measure_time = time.ticks_ms() # Μέτρα από την αρχή
        sensor1.measure()  # Πάρε τιμές θερμοκρασίας και υγρασίας
    if time.ticks_ms() - tele_time > TelePeriod: # Κάθε 1 - 5 λεπτά στείλε τηλεμετρία
        tele_time = time.ticks_ms() # Μέτρα από την αρχή
        if Relay1.value(): # Σε τι κατάσταση είναι η συσκευή
            t = 'POWER1:ON' # Σε λειτουργία
        else:
            t = 'POWER1:OFF' # Σβηστή
        # Ετοίμασε μήνυμα csv χωρισμένο με ';'
        t = get_time() + ";" + str(sensor1.temperature()) + ";" + str(sensor1.humidity()) + ";" + t
        client.publish(topic2_pub, t.encode()) # Δημοσίευσε το tele
        print("Tele: ", t.encode()) # Debug
        if ntp_sync <= 0:
            ntp_sync = NTP_SYNC
            print("Επανασυγχρονισμός NTP") # Debug
            ntptime.settime() # Συγχρονισμός
        else:
            ntp_sync -= 1
            