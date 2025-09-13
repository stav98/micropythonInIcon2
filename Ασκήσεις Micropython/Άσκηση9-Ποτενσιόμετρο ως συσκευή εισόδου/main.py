from machine import Pin, ADC
from time import sleep
from neopixel import NeoPixel

#Σταθερές χρωμάτων
RED = (255, 0, 0); GREEN = (0, 255, 0); BLUE = (0, 0, 255); YELLOW = (255, 255, 0)  
MAGENTA = (255, 0, 255); CYAN = (0, 255, 255); BLANK = (0, 0, 0)
AVG_FACTOR = 1.5 #Συντελεστής μέσης τιμής όσο μεγαλύτερος τόσο πιο αργή μεταβολή
avg_val = 0 #Μέση τιμή του ADC

pot = ADC(Pin(4)) #4, 26, 32, 34
pot.width(ADC.WIDTH_10BIT) #Ευκρίνεια 10BIT, 9BIT, 10BIT, 11BIT, 12BIT προκαθορισμένο
pot.atten(ADC.ATTN_11DB) # πλήρης κλίμακα έως 3.3V

np = NeoPixel(Pin(25), 5) #IO25, 5 x RGB Leds

#Λίστα με τις εντολές
C = ['Θέση - 1', 'Θέση - 2', 'Θέση - 3', 'Θέση - 4', 'Θέση - 5']
#Παράλληλη λίστα με τα χρώματα για κάθε θέση
COLORS = [RED, GREEN, BLUE, YELLOW, MAGENTA]
PLACES = len(C) #Υπολόγισε αριθμό θέσεων
THRESS = 5 #Κατώφλι υστέρησης
pos = 0 #Θέση στην λίστα με τις εντολές

#Η συνάρτηση σβήνει και τα 5 RGB Leds
def blank_leds():
  for i in range(5):
    np[i] = BLANK
  
#Συνάρτηση για να ανάβει τα Leds ανάλογα με την τιμή του ADC
def out_leds(n):
  blank_leds()
  np[4 - n] = COLORS[n]
  np.write()

#Η συνάρτηση επιλέγει εντολή ανάλογα με την τιμή του x δηλαδή την θέση του ποτενσιομέτρου
#Υπάρχει πρόβλεψη υστέρησης τιμής THRESS ώστε να μην παίζει η απόφαση τις εντολής σε γειτονικές
#τιμές. π.χ. αν είναι 127 και 128 τότε θα μεταβάλλεται από Θέση-1 σε Θέση-2. Με υστέρηση π.χ. 5
#για να αλλάξει σε Θέση-1 πρέπει να πέσει κάτω από 123 και για να ανέβει σε Θέση-2 πρέπει να
#ξεπεράσει το 133.
def get_command(x):
  global pos
  stp = 1024 // PLACES #Βήμα για κάθε θέση
  s = 0 #Άθροισμα βημάτων
  i = 0
  for i in range(8):
    if x > s + THRESS and x < s + stp - THRESS: #Αν ξέφυγε από την περιοχή υστέρησης τότε
      pos = i #Άλλαξε την τιμή του pos, διαφορετικά ισχύει η προηγούμενη τιμή
    s += stp
  return pos

#Για πάντα
while True:
  pot_value = pot.read() #Διάβασε τιμή ποτενσιομέτρου
  avg_val = int((AVG_FACTOR * avg_val + pot_value) / (AVG_FACTOR + 1)) #Μέση τιμή
  tmp = get_command(avg_val)
  print(C[tmp]) #Εμφάνισε εντολή
  out_leds(tmp)
  #print("τιμή:", avg_val) #Debug
  sleep(.1)