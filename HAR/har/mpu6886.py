# Untitled - By: Loza - ju. nov. 14 2019

## M5StickV MPU6886 maixpy
## Referred to the following
## https://github.com/m5stack/M5StickC/blob/master/src/utility/MPU6886.cpp
##https://github.com/m5stack/M5-Schematic/blob/master/datasheet/MPU-6886-000193%2Bv1.1_GHIC.PDF.pdf

from machine import I2C

MPU6886_ADDRESS=0x68
MPU6886_WHOAMI=0x75
MPU6886_ACCEL_INTEL_CTRL=  0x69
MPU6886_SMPLRT_DIV=0x19
MPU6886_INT_PIN_CFG=   0x37
MPU6886_INT_ENABLE=0x38
MPU6886_ACCEL_XOUT_H=  0x3B
MPU6886_TEMP_OUT_H=0x41
MPU6886_GYRO_XOUT_H=   0x43
MPU6886_USER_CTRL= 0x6A
MPU6886_PWR_MGMT_1=0x6B
MPU6886_PWR_MGMT_2=0x6C
MPU6886_CONFIG=0x1A
MPU6886_GYRO_CONFIG=   0x1B
MPU6886_ACCEL_CONFIG=  0x1C
MPU6886_ACCEL_CONFIG2= 0x1D
MPU6886_FIFO_EN=   0x23

i2c = I2C(I2C.I2C0, freq=100000, scl=28, sda=29)
devices = i2c.scan()
time.sleep_ms(10)

print("i2c",devices)

#tempdata = i2c.readfrom_mem(MPU6886_ADDRESS, MPU6886_WHOAMI,1)
#accel = i2c.readfrom_mem(MPU6886_ADDRESS, MPU6886_WHOAMI, 1)
#print ("ChipID:", accel);

tempdata = 0x00
i2c.writeto_mem(MPU6886_ADDRESS, MPU6886_PWR_MGMT_1, bytearray([tempdata]))
time.sleep_ms(10)

tempdata = 0x01<<7
i2c.writeto_mem(MPU6886_ADDRESS, MPU6886_PWR_MGMT_1, bytearray([tempdata]))
time.sleep_ms(10)

tempdata = 0x01<<0
i2c.writeto_mem(MPU6886_ADDRESS, MPU6886_PWR_MGMT_1, bytearray([tempdata]))
time.sleep_ms(10)

tempdata = 0x10
i2c.writeto_mem(MPU6886_ADDRESS, MPU6886_ACCEL_CONFIG, bytearray([tempdata]))
time.sleep_ms(1)

tempdata = 0x18
i2c.writeto_mem(MPU6886_ADDRESS, MPU6886_GYRO_CONFIG, bytearray([tempdata]))
time.sleep_ms(1)

tempdata = 0x01
i2c.writeto_mem(MPU6886_ADDRESS, MPU6886_CONFIG, bytearray([tempdata]))
time.sleep_ms(1)

tempdata = 0x05
i2c.writeto_mem(MPU6886_ADDRESS, MPU6886_SMPLRT_DIV, bytearray([tempdata]))
time.sleep_ms(1)

tempdata = 0x00
i2c.writeto_mem(MPU6886_ADDRESS, MPU6886_INT_ENABLE, bytearray([tempdata]))
time.sleep_ms(1)

tempdata = 0x00
i2c.writeto_mem(MPU6886_ADDRESS, MPU6886_ACCEL_CONFIG2, bytearray([tempdata]))
time.sleep_ms(1)

tempdata = 0x00
i2c.writeto_mem(MPU6886_ADDRESS, MPU6886_USER_CTRL, bytearray([tempdata]))
time.sleep_ms(1)
tempdata = 0x00
i2c.writeto_mem(MPU6886_ADDRESS, MPU6886_FIFO_EN, bytearray([tempdata]))
time.sleep_ms(1)

tempdata = 0x22
i2c.writeto_mem(MPU6886_ADDRESS, MPU6886_INT_PIN_CFG, bytearray([tempdata]))
time.sleep_ms(1)

tempdata = 0x01
i2c.writeto_mem(MPU6886_ADDRESS, MPU6886_INT_ENABLE, bytearray([tempdata]))
time.sleep_ms(100)

aRes = 8.0/32768.0;
gRes = 2000.0/32768.0;
while True:
    time.sleep_ms(100)
    accel = i2c.readfrom_mem(MPU6886_ADDRESS, MPU6886_ACCEL_XOUT_H, 6)
    accel_x = (accel[0]<<8|accel[1])
    accel_y = (accel[2]<<8|accel[3])
    accel_z = (accel[4]<<8|accel[5])
    if accel_x>32768:
        accel_x=accel_x-65536
    if accel_y>32768:
        accel_y=accel_y-65536
    if accel_z>32768:
        accel_z=accel_z-65536
    accel_array = [accel_x*aRes, accel_y*aRes, accel_z*aRes]

    gyro = i2c.readfrom_mem(MPU6886_ADDRESS, MPU6886_GYRO_XOUT_H, 6)
    gyro_x = (gyro[0]<<8|gyro[1])
    gyro_y = (gyro[2]<<8|gyro[3])
    gyro_z = (gyro[4]<<8|gyro[5])
    if gyro_x>32768:
        gyro_x=gyro_x-65536
    if gyro_y>32768:
        gyro_y=gyro_y-65536
    if gyro_z>32768:
        gyro_z=gyro_z-65536

    gyro_array = [gyro_x*gRes, gyro_y*gRes, gyro_z*gRes]

    temp = i2c.readfrom_mem(MPU6886_ADDRESS, MPU6886_TEMP_OUT_H, 2)
    temp_dat = (temp[0]<<8| temp[1])
    print(accel_array,"_",gyro_array,"_",temp_dat)
