import machine, time, socket, network, gc, esp, neopixel
esp.osdebug(None)
gc.collect()
ssid = 'SSID' #Το SSID του τοπικού δικτύου WiFi
password = 'Password' #Ο κωδικός του WiFi
station = network.WLAN(network.STA_IF) #Θα λειτουργήσει σαν σταθμός ώστε να συνδεθεί στο AP

station.active(True) #Ενεργοποίηση
station.connect(ssid, password) #Σύνδεση

while station.isconnected() == False: #Περίμενε μέχρι να συνδεθεί
    pass

print('Connection successful')
print(station.ifconfig())

np = neopixel.NeoPixel(machine.Pin(25), 5) #IO25, 5 x RGB Leds
led_state = False

#Ανάβει άσπρα τα 5 Led της πλακέτας
def led_ON():
    global led_state
    for i in range(5):
        np[i] = (255, 255, 255) #Άσπρο
    led_state = True
    np.write()

#Σβήνει τα 5 Led της πλακέτας
def led_OFF():
    global led_state
    for i in range(5):
        np[i] = (0, 0, 0) #Σβηστό
    led_state = False
    np.write()

#Η ιστοσελίδα που επιστρέφει στον browser
def web_page():
    if led_state == True:
        cur_state="ON"
    else:
        cur_state="OFF"
    html = """
<!DOCTYPE HTML>
<html>
 <head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <title>ESP Web Server</title> 
  <meta name="viewport" content="width=device-width, initial-scale=1">
 </head>
 <body> 
  <center><h1>Δοκιμή WEB Server</h1></center> 
  <p><center>Κατάσταση: <strong>""" + cur_state + """</strong></center></p>
  <p><center><a href="/?led=on"><button>ON</button></a>&nbsp;
  <a href="/?led=off"><button>OFF</button></a></center></p>
 </body>
</html>"""
    return html

s = socket.socket() #Δημιουργία υποδοχής TCP (Socket)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Options
s.bind(('', 80)) #Ακούει από οποιαδήποτε διεύθυνση IP - Θύρα 80 HTTP 
s.listen(5) #Ακούει μέχρι 5 ταυτόχρονες συνδέσεις

while True: #Για πάντα
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024) #Το αίτημα μέχρι 1024 bytes
    request = str(request) #Να γίνει string από byte array
    #print('Content = %s' % request) #Debug
    request = request.split()[1] #Χώρισέ το στα κενά και πάρε το 2ο στοιχείο της λίστας
    if request == '/?led=on': #Αν υπάρχει αίτημα on
        print('LED ON')
        led_ON() #Άναψε τα Led
    elif request == '/?led=off': #Διαφορετικά αν υπάρχει αίτημα off
        print('LED OFF')
        led_OFF() #Σβήσε τα Led
    response = web_page() #Ετοίμασε σελίδα για απάντηση
    conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n') #Επικεφαλίδα HTTP
    conn.send(response) #Στείλε πίσω στον browser την σελίδα
    conn.close() #Κλείσε σύνδεση
