import machine
import time
import lcd
import utime
from machine import I2C

i2c = I2C(I2C.I2C0, freq=100000, scl=28, sda=29)
devices = i2c.scan()
print("IC2:", devices)

time.sleep(1)

# FIFO reset
i2c.writeto_mem(108, 0x12, bytearray([0]))

# Chip ID
tempdata = i2c.readfrom_mem(108, 0x30, 1)
print ("ChipID:", tempdata[0])

time.sleep(1)

tempdata = i2c.readfrom_mem(108, 0xC2, 1)

tempdata = tempdata[0] | 0x04
i2c.writeto_mem(108, 0xC2, bytearray([tempdata]));
time.sleep(1)

tempdata = tempdata | 0xFB
i2c.writeto_mem(108, 0xC2, bytearray([tempdata]));

#
tempdata = i2c.readfrom_mem(108, 0xD8, 1)
tempdata = tempdata[0] | 0x80
i2c.writeto_mem(108, 0xD8, bytearray([tempdata]));
time.sleep(1)

tempdata = tempdata & 0x7F;
i2c.writeto_mem(108, 0xD8, bytearray([tempdata]));
i2c.writeto_mem(108, 0x78, bytearray([0x61]));
time.sleep(1)
i2c.writeto_mem(108, 0x78, bytearray([0x00]));

# set acc odr 256hz
i2c.writeto_mem(108, 0x0e, bytearray([0x91]));

# set gyro odr 500hz
i2c.writeto_mem(108, 0x0f, bytearray([0x13]));

# set gyro dlpf 50hz
i2c.writeto_mem(108, 0x11, bytearray([0x03]));

# set no buffer mode
i2c.writeto_mem(108, 0x12, bytearray([0x00]));

# set acc range +-8G
i2c.writeto_mem(108, 0x16, bytearray([0x01]));

# set gyro range +-2000¶È/s
i2c.writeto_mem(108, 0x2B, bytearray([0x00]));

i2c.writeto_mem(108, 0xBA, bytearray([0xC0]));
tempdata = i2c.readfrom_mem(108, 0xCA, 1)
tempdata = tempdata[0] | 0x10

# ADC Reset
i2c.writeto_mem(108, 0xCA, bytearray([tempdata]));
time.sleep(1)

tempdata = tempdata | 0xEF
i2c.writeto_mem(108, 0xCA, bytearray([tempdata]));
time.sleep(10)

# LCD
lcd.init()

# file open
file = open('standing.csv', 'w')

MODE = "Standing"

# get acceralator data.
while True:
    lcd.clear()
    accel = i2c.readfrom_mem(108, 0x00, 6)
    accel_x = accel[1]
    accel_y = accel[3]
    accel_z = accel[5]

    print ("accel:", accel_x, accel_y, accel_z)
    file.write("1," + MODE + ",0," + str(accel_x) + "," + str(accel_y) + "," + str(accel_z) + "\n")
    utime.sleep_ms(30)
    file.flush()

file.close()
