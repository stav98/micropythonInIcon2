from machine import Pin, ADC
from time import sleep

#Αισθητήρας Hall DJS07 στο pin IO4
hall = Pin(4, Pin.IN, Pin.PULL_UP)
#LED DJX01 στο pin IO32
light = Pin(32, Pin.OUT) #Ψηφιακή έξοδος
light.value(0) #Σβηστό

#Για πάντα
while True:
  state = hall.value()
  print("Κατάσταση Hall: ", state) #Εμφάνισε κατάσταση αισθητήρα Hall
  if not state: #Αν είναι 0 έχει πλησιάσει ο μαγνήτης
     light.value(1) #Άναψε το LED
  else: #Διαφορετικά δεν υπάρχει ικανό μαγνητικό πεδίο 
     light.value(0) #Σβήσε το LED
  sleep(1) #Περίμενε 1 sec
