import machine, time
threshold = 150 #Κατώφλι. Τιμές κάτω από εδώ σημαίνουν ότι πατήθηκε
touch_pin = machine.TouchPad(machine.Pin(12)) #Το πρώτο κουμπί

print("\nESP32 Touch Demo")
while True: # Για πάντα
  capacitiveValue = touch_pin.read() #Διάβασε τιμές
  if capacitiveValue < threshold: #Είναι κάτω από το κατώφλι
    print("Με πάτησες")
    time.sleep_ms(500)