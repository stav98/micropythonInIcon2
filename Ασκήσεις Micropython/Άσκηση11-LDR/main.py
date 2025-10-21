from machine import Pin, ADC
from time import sleep

#Αντίσταση LDR από 600K στο σκοτάδι έως 200Ω σε δυνατό φως
ldr = ADC(Pin(4)) #4, 26, 32, 34
ldr.width(ADC.WIDTH_12BIT) #Ευκρίνεια 10BIT, 9BIT, 10BIT, 11BIT, 12BIT προκαθορισμένο
ldr.atten(ADC.ATTN_11DB) # πλήρης κλίμακα έως 3.3V
#LED DJX01 στο pin IO32
light = Pin(32, Pin.OUT) #Ψηφιακή έξοδος
light.value(0) #Σβηστό

#Για πάντα
while True:
  vo = ldr.read() #Διάβασε τιμή της τάσης του διαιρέτη
  #Οι τιμές είναι από 0 (απόλυτο σκοτάδι) έως 4095 (δυνατό φως)
  print("Τιμή LDR: ", vo) #Εμφάνισε τιμή ADC
  if vo < 500: #Δυνατότητα υστέρησης για αποφυγή αναλαμπών
    light.value(1) #Άναψε το LED
  elif vo > 800:
    light.value(0) #Σβήσε το LED
  sleep(2) #Περίμενε 2 sec
