from machine import Pin, ADC
from time import sleep
from neopixel import NeoPixel

RED = (255, 0, 0); GREEN = (0, 255, 0); BLUE = (0, 0, 255); BLANK = (0, 0, 0)
AVG_FACTOR = 3 #Συντελεστής μέσης τιμής όσο μεγαλύτερος τόσο πιο αργή μεταβολή
avg_val = 0

pot = ADC(Pin(4)) #4, 26, 32, 34
pot.width(ADC.WIDTH_10BIT) #Ευκρίνεια 10BIT, 9BIT, 10BIT, 11BIT, 12BIT προκαθορισμένο
pot.atten(ADC.ATTN_11DB) # πλήρης κλίμακα έως 3.3V

np = NeoPixel(Pin(25), 5) #IO25, 5 x RGB Leds

#Συνάρτηση παρόμοια με την map του Arduino
#Δέχεται τρέχουσα τιμή, ελάχιστη τιμή, μέγιστη τιμή, έξοδος από, έως
def map(value, in_min, in_max, out_min, out_max):
  scaled_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  return int(scaled_value) #Επιστρέφει ακέραιο

#Συνάρτηση για να ανάβει τα Leds ανάλογα με την τιμή του ADC
def out_leds(x):
  n = x // 205 #Γιατί 1024 / 5 leds = 204,8 ακέραια διαίρεση
  y = x % 205 #Υπόποιπο για το τελευταίο Led
  i = 0
  while i < n: #Ανάβει πλήρως όσα Led υπολογίστηκαν στο n
    np[4 - i] = RED #Ανάβουν ανάποδα
    i += 1
  a = i #Κράτησε την τρέχουσα τιμή του i
  while i < 5: #Αν δεν είναι να ανάψουν όλα τότε σβήσε τα υπόλοιπα
    np[4 - i] = BLANK #Σβήνουν ανάποδα
    i += 1
  print(n, y, map(y, 0, 204, 2, 255))
  i = a #Επαναφορά του i
  if i <= 4: #Αν είναι από 0 έως 4 τότε άναψε μερικώς αυτό το Led
    np[4 - i] = (map(y, 0, 204, 2, 250), 0, 0) #Αλλαγή κλίμακας από 0-204 σε 2-255 για το κόκκινο (255 πλήρης ένταση)
  np.write()

#Για πάντα
while True:
  pot_value = pot.read() #Διάβασε τιμή ποτενσιομέτρου
  avg_val = int((AVG_FACTOR * avg_val + pot_value) / (AVG_FACTOR + 1)) #Μέση τιμή
  out_leds(avg_val) #Άναψε τα Leds
  print("τιμή:", avg_val)
  sleep(.1)