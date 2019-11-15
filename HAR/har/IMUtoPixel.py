# Untitled - By: Loza - ju. nov. 14 2019

## Copyright (c) 2019 aNoken
## https://twitter.com/anoken2017


import os, sys, time

sys.path.append('')
sys.path.append('.')

# chdir to "/sd" or "/flash"
devices = os.listdir("/")
if "sd" in devices:
    os.chdir("/sd")
    sys.path.append('/sd')
else:
    os.chdir("/flash")
sys.path.append('/flash')

print("[MaixPy] init end") # for IDE
for i in range(200):
    time.sleep_ms(1) # wait for key interrupt(for maixpy ide)

# check IDE mode
ide_mode_conf = "/flash/ide_mode.conf"
ide = True
try:
    f = open(ide_mode_conf)
    f.close()
except Exception:
    ide = False

if ide:
    os.remove(ide_mode_conf)
    from machine import UART
    import lcd
    lcd.init(color=lcd.PINK)
    repl = UART.repl_uart()
    repl.init(1500000, 8, None, 1, read_buf_len=2048, ide=True, from_ide=False)
    sys.exit()

import gc, uos, sys
import machine
from board import board_info
from fpioa_manager import fm
from pye_mp import pye
from Maix import FPIOA, GPIO

import sensor, image, time,lcd,machine
from machine import I2C

# I2C Check
i2c = I2C(I2C.I2C0, freq=100000, scl=28, sda=29)
devices = i2c.scan()
print(devices)
lcd.init()

# LCD Backlight
AXP192_ADDR=0x34
Backlight_ADDR=0x91
level=50
val = (level+7) << 4
i2c.writeto_mem(AXP192_ADDR, Backlight_ADDR,int(val))

# IMU6866 define
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


# IMU6866 Initialize
def write_i2c(address, value):
    i2c.writeto_mem(MPU6886_ADDRESS, address, bytearray([value]))
    time.sleep_ms(10)

write_i2c(MPU6886_PWR_MGMT_1, 0x00)
write_i2c(MPU6886_PWR_MGMT_1, 0x01<<7)
write_i2c(MPU6886_PWR_MGMT_1,0x01<<0)
write_i2c(MPU6886_ACCEL_CONFIG,0x10)
write_i2c(MPU6886_GYRO_CONFIG,0x18)
write_i2c(MPU6886_CONFIG,0x01)
write_i2c(MPU6886_SMPLRT_DIV,0x05)
write_i2c(MPU6886_INT_ENABLE,0x00)
write_i2c(MPU6886_ACCEL_CONFIG2,0x00)
write_i2c(MPU6886_USER_CTRL,0x00)
write_i2c(MPU6886_FIFO_EN,0x00)
write_i2c(MPU6886_INT_PIN_CFG,0x22)
write_i2c(MPU6886_INT_ENABLE,0x01)

# Button_A
fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)

# Button_B
fm.register(board_info.BUTTON_B, fm.fpioa.GPIO2)
but_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)

but_a_pressed = 0
but_b_pressed = 0


# Read IMU6866 and Scaling
def read_imu():
    aRes=255/4096/2
    offset=128
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
    ax=int(accel_x*aRes+offset)
    if ax<0: ax=0
    if ax>255: ax=255
    ay=int(accel_y*aRes+offset)
    if ay<0: ay=0
    if ay>255: ay=255
    az=int(accel_z*aRes+offset)
    if az<0: az=0
    if az>255: az=255
    accel_array = [ay,az,ax]
    return accel_array

cnt=0
mode=0
save_flg=0
pic_no=0
accel_array_zero=(255,255,255)

#IMU_Image
w_size=8
view_size=120
imu_Image = image.Image()
imu_Image = imu_Image.resize(w_size, w_size)
image_data_array = []

while(True):
    view_Image = image.Image()

    # IMU Data to Image
    accel_array = read_imu()
    w=cnt%w_size
    h=int(cnt/w_size)
    imu_Image.set_pixel(w, h, accel_array)
    width=imu_Image.width()

    # IMU Data_View
    w=(cnt+1)%w_size
    h=int((cnt+1)/w_size)
    imu_Image.set_pixel(w, h, accel_array_zero)
    img_buff=imu_Image.resize(view_size,view_size)
    view_Image.draw_image(img_buff,100,8)

    #imu_Image.pix_to_ai()

    if save_flg==1:
        view_Image.draw_string(0, 40, "REC", (255,0,0),scale=3)
        class_str=str(mode);
        view_Image.draw_string(0, 70,class_str, (255,0,0),scale=5)
        if cnt%width<width/2:
            view_Image.draw_circle(30, 15, 15,(255,0,0),fill=1)

    lcd.display(view_Image)

    cnt=cnt+1


    # IMU Data Save to SD
    if cnt>imu_Image.width()*imu_Image.height():
        cnt=0
        pic_no+=1
        if save_flg==1:
            cnt_str="{0:04d}".format(pic_no)
            mode_str="{0:04d}".format(mode)
            fname="cnt_str"+mode_str+"_"+cnt_str+".jpg"
            print(fname)
            imu_Image.save(fname, quality=99)

    if but_a.value() == 0 and but_a_pressed == 0:
        but_a_pressed=1
        if save_flg==0:
            save_flg=1
            print("save_start")
        elif save_flg==1:
            save_flg=0

    if but_a.value() == 1 and but_a_pressed == 1:
        but_a_pressed=0

    if but_b.value() == 0 and but_b_pressed == 0:
        but_b_pressed=1
        mode+=1
        if mode>10:
            mode=0
    if but_b.value() == 1 and but_b_pressed == 1:
        but_b_pressed=0
