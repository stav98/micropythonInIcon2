import machine, neopixel, asyncio

# Προετοιμασία RGB Led
np = neopixel.NeoPixel(machine.Pin(25), 5) #IO25, 5 x RGB Leds
led_status = [0, 0, 0, 0, 0] #Λίστα με την κατάσταση των Led (0=σβηστό, 1=αναμμένο)
RED = (255, 0, 0) #Κόκκινο
GREEN = (0, 255, 0) #Πράσινο
BLUE = (0, 0, 255) #Μπλε

# Η συνάρτηση αναβοσβήνει το Led με αριθμό num (0-4) με το χρώμα color
def toggle_Led(num, color):
    if led_status[num] == 0: #Είναι σβηστό
        np[num] = color #Γράψε χρώμα
        led_status[num] = 1 #Σημείωσε ότι τώρα είναι αναμμένο
    else: #Διαφορετικά είναι αναμμένο
        np[num] = (0, 0, 0) #Σβήσε (0,0,0) = σβηστό (μαύρο)
        led_status[num] = 0 #Σημείωσε ότι τώρα είναι σβηστό
    np.write() #Στείλε εντολή στα LED

# Ασύγχρονη λειτουργία (coroutine) για Πράσινο
async def blink_green_led():
    while True: #Για πάντα
        toggle_Led(4, GREEN) #Αναβόσβησε το 1ο στην σειρά με χρώμα πράσινο
        await asyncio.sleep(2) #Περίμενε 2 sec και δώσε την δυνατότητα εκτέλεσης άλλων λειτουργιών

# Ασύγχρονη λειτουργία (coroutine) για Κόκκινο
async def blink_red_led():
    while True:
        toggle_Led(0, RED) #Αναβόσβησε το 5ο στην σειρά με χρώμα κόκκινο
        await asyncio.sleep(0.5) #Περίμενε .5 sec και δώσε την δυνατότητα εκτέλεσης άλλων λειτουργιών

# Ασύγχρονη λειτουργία (coroutine) για Μπλε
async def blink_blue_led():
    while True: #Για πάντα
        toggle_Led(2, BLUE) #Αναβόσβησε το μεσαίο με χρώμα μπλε
        await asyncio.sleep(0.1) #Περίμενε 100 msec και δώσε την δυνατότητα εκτέλεσης άλλων λειτουργιών

# Ορισμός της συνάρτησης main που περιέχει το event loop
async def main():
    # Δημιουργία εργασιών (tasks) ώστε να αναβοσβήνουν τα 3 Led ταυτόχρονα
    asyncio.create_task(blink_green_led())
    asyncio.create_task(blink_red_led())
    asyncio.create_task(blink_blue_led())

# Δημιουργία και εκτέλεση του event loop
loop = asyncio.get_event_loop()  
loop.create_task(main())  # Δημιουργία εργασίας (task) που εκτελεί το event loop
loop.run_forever()  # Τρέξε για πάντα