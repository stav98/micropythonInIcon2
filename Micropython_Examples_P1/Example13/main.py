from MPU6050 import MPU6050

from machine import Pin
from time import sleep_ms

mpu = MPU6050()

# Για πάντα    
while True:
    # Επιταχυνσιόμετρο
    #'''
    accel = mpu.read_accel_data() # Διάβασε το επιταχυνσιόμετρο [m / s^2]
    aX = accel["x"]
    aY = accel["y"]
    aZ = accel["z"]
    print("x: " + str(aX) + " y: " + str(aY) + " z: " + str(aZ))
    #'''
    
    # Γυροσκόπιο
    '''
    gyro = mpu.read_gyro_data()   # Διάβασε το γυροσκόπιο [deg/s]
    gX = gyro["x"]
    gY = gyro["y"]
    gZ = gyro["z"]
    print("x:" + str(gX) + " y:" + str(gY) + " z:" + str(gZ))
    '''
    
    # Θερμοκρασία
    #temp = mpu.read_temperature()   # Διάβασε την θερμοκρασία της συσκευής [degC]
    #print("Θερμοκρασία: " + str(temp) + "°C")

    # G-Force
    #gforce = mpu.read_accel_abs(g=True) # Διάβασε το μέτρο της επιτάχυνσης
    #print("G-Force: " + str(gforce))
        
    # Χρόνος παύσης σε (ms)
    sleep_ms(100)