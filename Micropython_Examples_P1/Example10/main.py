import machine, time
i2c = machine.I2C(0, sda = machine.Pin(21), scl = machine.Pin(22), freq = 400000)
#Ή εναλλακτικά
#i2c = machine.SoftI2C(sda=machine.Pin(21), scl=machine.Pin(22))

from gesture import Gesture
g=Gesture(i2c)
# 	0: Τίποτα
# 	1: Μπροστά 
# 	2: Πίσω
# 	3: Δεξιά
# 	4: Αριστερά
# 	5: Πάνω
# 	6: Κάτω
# 	7: Περιστροφή σύμφωνα με τους δείκτες του ρολογιού
# 	8: Περιστροφή αντίθετα με τους δείκτες του ρολογιού
# 	9: Κυματισμός

while 1:
    #g.print_gesture() #Εμφανίζει την χειρονομία
    value=g.return_gesture()
    #print(value) #Debug
    #if value==0:
    #    print("Αδράνεια")  # nothing
    if value==1:
        print("Μπροστά") #Το χέρι κινείται από πάνω προς τον αισθητήρα (άξονας Z)
    if value==2:
        print("Πίσω") #Το χέρι κινείται από τον αισθητήρα προς τα πάνω (άξονας Z)
    if value==3:
        print("Δεξιά") #Δεξιά (άξονας X)
    if value==4:
        print("Αριστερά") #Αριστερά (άξονας X)
    if value==5:
        print("Πάνω") #Πάνω (άξονας Y)
    if value==6:
        print("Κάτω") #Κάτω (άξονας Y)
    if value==7:
        print("Δείκτες ρολογιού") #Περιστροφή (άξονας X-Y)
    if value==8:
        print("Αντίθετα από δείκτες ρολογιού") #Αντίθετη περιστροφή (άξονας X-Y)
    if value==9:
        print("Κυματισμός") #Γρήγορα πάνω κάτω άξονα Y 
    time.sleep(1)