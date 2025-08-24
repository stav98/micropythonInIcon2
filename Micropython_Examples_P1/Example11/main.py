import machine, os

sd = machine.SDCard(slot=2, width=1, sck=18, miso=19, mosi=23, cs=2, freq=40000000) #SPI
#Πληροφορίες κάρτας SD
sdsize = sd.info() #Ο πρώτος αριθμός είναι η συνολική χωρητικότητα σε Gb και ο δεύτερος το μέγεθος τομέα (512)
print("Μνήμη SD: ", round(sdsize[0] / 1000000000), "GB")

vfs.mount(sd, "/sd") #Προσάρτηση τόμου στο mountpoint
stat = os.statvfs('/sd') #Πληροφορίες κατάτμησης
print("Συνολικός χώρος κατάτμησης:", round(stat[0] * stat[2] / 1000000000, 1), "GB")
print("Σε χρήση:", round(stat[0] * (stat[2] - stat[3]) / 1000000000, 1), "GB")

os.chdir('sd') #Αλλαγή στο mountpoint
print(os.listdir()) #Εμφάνιση αρχείων καταλόγου
#vfs.umount('/sd') #Αποπροσάρτηση τόμου