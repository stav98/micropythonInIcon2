from micropython import const
import bluetooth, aioble, struct, asyncio
import machine, neopixel, dht
from random import randint

# Προετοιμασία RGB Led
np = neopixel.NeoPixel(machine.Pin(25), 5) #IO25, 5 x RGB Leds
OFF = (0, 0, 0)
ON = (255, 255, 255)
np[0] = OFF
np.write()

#Αισθητήρας DHT11
dht_sensor = dht.DHT11(machine.Pin(33))

# Η πλακέτα λειτουργεί ως περιφερειακό και ο τύπος συσκευής είναι διακομιστής εκθέτοντας 
# τη δομή GATT που περιέχει δεδομένα. Το κινητό είναι controller με τύπο client
# Διεύθυνση για παραγωγή UUIDs: https://www.uuidgenerator.net/
_BLE_SERVICE_UUID = bluetooth.UUID('cc9d5ed0-c492-4d14-aefe-05941c6e2f71')
_BLE_TEMP_SENSOR_CHAR_UUID = bluetooth.UUID('a2738918-65a4-4dc1-9d5a-8779a23373c7')
_BLE_HUM_SENSOR_CHAR_UUID = bluetooth.UUID('de82b0bc-4a19-4a91-a9fd-fd5c0bd6a5e2')
_BLE_LED_UUID = bluetooth.UUID('22abbaa8-0b85-4bf9-9e97-e81fec3f9ecb')
# Πόσο συχνά εκπέμπει advertising beacons.
_ADV_INTERVAL_MS = 250_000 #250000 msecs

# Καταχώρηση διακομιστή δομής GATT, της υπηρεσίας και των χαρακτηριστικών
ble_service = aioble.Service(_BLE_SERVICE_UUID)
sensorT_characteristic = aioble.Characteristic(ble_service, _BLE_TEMP_SENSOR_CHAR_UUID, 
read = True, notify = True)
sensorH_characteristic = aioble.Characteristic(ble_service, _BLE_HUM_SENSOR_CHAR_UUID, 
read = True, notify = True)
led_characteristic = aioble.Characteristic(ble_service, _BLE_LED_UUID, 
read = True, write = True, notify = True, capture = True)

# Καταχώρηση υπηρεσίας BLE
aioble.register_services(ble_service)

# Κωδικοποίηση των δεδομένων των χαρακτηριστικών σε UTF-8 για αποστολή
def _encode_data(data):
    return str(data).encode('utf-8')

# Αποκωδικοποίηση του χαρακτηριστικού του LED από bytes σε αριθμό κατά την λήψη
def _decode_data(data):
    if data is not None:
        # Αποκωδικοποίηση από bytes σε ακέραιο
        number = int.from_bytes(data, 'big')
        return number

# Διάβασε δεδομένα από DHT11
def get_sensor_value():
    dht_sensor.measure() # Διάβασε τιμή αισθητήρα
    return dht_sensor.temperature(), dht_sensor.humidity() # Επιστροφή τιμών

# Διάβασε νέα τιμή και στείλε στο χαρακτηριστικό sensor
async def sensor_task():
    while True:
        value1, value2 = get_sensor_value()
        sensorT_characteristic.write(_encode_data(value1), send_update = True)
        sensorH_characteristic.write(_encode_data(value2), send_update = True)
        print('θερμοκρασία: ', value1, 'Υγρασία: ', value2)
        await asyncio.sleep_ms(2000) # Περίμενε 2sec για την επόμενη αποστολή
        
# Περίμενε για συνδέσεις. Μην διαφημίζεις αν υπάρχει σύνδεση με controller
async def peripheral_task():
    while True:
        try:
            async with await aioble.advertise(
                _ADV_INTERVAL_MS,
                name = "ARD_ICON_II",
                services = [_BLE_SERVICE_UUID],
                ) as connection:
                    print("Σύνδεση από:", connection.device)
                    await connection.disconnected()             
        except asyncio.CancelledError:
            # Catch the CancelledError
            print("Peripheral task cancelled")
        except Exception as e:
            print("Error in peripheral_task:", e)
        finally:
            # Ensure the loop continues to the next iteration
            await asyncio.sleep_ms(100)

# Περίμενε για εντολή στο χαρακτηριστικό του LED από controller
async def wait_for_write():
    while True:
        try:
            connection, data = await led_characteristic.written()
            print(data) #Debug
            print(type(data)) #Debug
            data = _decode_data(data)
            print('Connection: ', connection)
            print('Data: ', data)
            if data == 1:
                print('Το LED άναψε')
                np[0] = ON
                np.write()
            elif data == 0:
                print('Το LED έσβησε')
                np[0] = OFF
                np.write()
            else:
                print('Άγνωστη εντολή')
        except asyncio.CancelledError:
            # Catch the CancelledError
            print("Peripheral task cancelled")
        except Exception as e:
            print("Error in peripheral_task:", e)
        finally:
            # Ensure the loop continues to the next iteration
            await asyncio.sleep_ms(100)
            
# Εκτέλεση των διεργασιών
async def main():
    t1 = asyncio.create_task(sensor_task())
    t2 = asyncio.create_task(peripheral_task())
    t3 = asyncio.create_task(wait_for_write())
    await asyncio.gather(t1, t2)
    
asyncio.run(main())