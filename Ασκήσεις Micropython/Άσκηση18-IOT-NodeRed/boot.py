import time, network, gc, esp

esp.osdebug(None)
gc.collect()
ssid = 'SSID' #Το SSID του τοπικού δικτύου WiFi
password = 'WifiKEY' #Ο κωδικός του WiFi
station = network.WLAN(network.STA_IF) #Θα λειτουργήσει σαν σταθμός ώστε να συνδεθεί στο AP

station.active(True) #Ενεργοποίηση
station.connect(ssid, password) #Σύνδεση

while station.isconnected() == False: #Περίμενε μέχρι να συνδεθεί
    pass

print('Connection successful')
print(station.ifconfig())

time.sleep(1) # Περίμενε 1sec μέχρι να γίνει η σύνδεση και μετά συνέχισε
