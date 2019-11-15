import sensor,lcd,image
import KPU as kpu


lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.set_hmirror(1)
sensor.set_windowing((128, 128))    #set to 224x224 input
sensor.run(1)
# sensor.set_hmirror(0)               #flip camera
task = kpu.load(0x300000)           #load model from flash address 0x300000
while True:
    img = sensor.snapshot()
    lcd.display(img,oft=(0,0))      #display large picture
    img1=img.to_grayscale(1)        #convert to gray
    img2=img1.resize(28,28)         #resize to mnist input 28x28
    a=img2.invert()                 #invert picture as mnist need
    a=img2.strech_char(1)           #preprocessing pictures, eliminate dark corner
    prev = img2.resize(100,100)
    lcd.display(prev,oft=(128,32))  #display small 28x28 picture
    a=img2.pix_to_ai();             #generate data for ai
    fmap=kpu.forward(task,img2)     #run neural network model
    plist=fmap[:]                   #get result (10 digit's probability)
    pmax=max(plist)                 #get max probability
    print(plist)
    max_index=plist.index(pmax)     #get the digit
    lcd.draw_string(224,0,"%d: %.3f"%(max_index,pmax),lcd.WHITE,lcd.BLACK)  #show result
