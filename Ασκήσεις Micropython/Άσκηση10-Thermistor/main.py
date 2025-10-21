from machine import Pin, ADC
from dht import DHT11
from time import sleep
import math

R2 = 4660 #Ωμ
Vi = 3.27 #Volts

#Σταθερές Steinhart για το NTC Thermistor TCS610
A = 1.1279e-03 #0.001129148
B = 2.3429e-04 #0.000234125
C = 8.7298E-08 #0.0000000876741

ntc = ADC(Pin(4)) #4, 26, 32, 34
ntc.width(ADC.WIDTH_12BIT) #Ευκρίνεια 10BIT, 9BIT, 10BIT, 11BIT, 12BIT προκαθορισμένο
ntc.atten(ADC.ATTN_11DB) # πλήρης κλίμακα έως 3.3V

sensor = DHT11(Pin(33)) #DHT11 για σύγκριση
sensor.measure() #Νέα μέτρηση του DHT11

#Για πάντα
while True:
  vo = ntc.read() #Διάβασε τιμή της τάσης του διαιρέτη
  vo /= .9 #Διόρθωση μη γραμμικής συμπεριφοράς ADC
  Rntc = R2 * (4095.0 / vo - 1); #Υπολογισμός αντίστασης NTC
  #Υπολογισμός θερμοκρασίας σε βαθμούς Kelvin
  TempK = 1 / (A + (B * math.log(Rntc)) + C * math.pow(math.log(Rntc), 3))
  TempC = TempK - 273.15 #Μετατροπή σε °C
  print("Θερμοκρασία NTC: ", round(TempC, 2), "°C") #Εμφάνισε Θερμοκρασία NTC
  print("Θερμοκρασία DHT11:", sensor.temperature() + 1.0, "°C\n")
  sleep(2) #Περίμενε 2 sec
