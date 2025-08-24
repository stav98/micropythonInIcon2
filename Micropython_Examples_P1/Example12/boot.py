import machine, os

sd = machine.SDCard(slot=2, width=1, sck=18, miso=19, mosi=23, cs=2, freq=40000000) #SPI
#Πληροφορίες κάρτας SD
sdsize = sd.info() #Ο πρώτος αριθμός είναι η συνολική χωρητικότητα σε Gb και ο δεύτερος το μέγεθος τομέα (512)
print("Μνήμη SD: ", round(sdsize[0] / 1000000000), "GB")

vfs.mount(sd, "/sd") #Προσάρτηση τόμου στο mountpoint

os.chdir('sd') #Αλλαγή στο mountpoint
import start