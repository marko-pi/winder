import pigpio
import time

pise = 25                # servo pin
piha = 27                # Hall detector pin
pimi = 5                 # plus pin
pipl = 6                 # minus pin
pire = 13                # reset pin
spd = 0                  # current rotation speed
nspd = 0                 # new rotation speed
mcnt = 0                 # magnet counter
mtim = time.time()       # time at last magnet event
butb = time.time()       # time at last both buttons
buto = time.time()       # time at last one button

def mwri(num, pos, siz=1):
    lst=[]
    mns = False
    if num < 0: mns = True
    num = abs(num)
    if num == 0: lst.insert(0,0)
    while num != 0:
        lst.insert(0,num % 10)
        num=num//10
    if mns: lst.insert(0,10)
    for i in range(siz-len(lst)):
        lst.insert(0,-1)
    for i in range(len(lst)):
        mypi.spi_xfer(cont, [9-pos-i, mnum[lst[i]]])

def magn(gpio, level, tick):
    global mcnt
    global mtim

    if time.time()-mtim > 1:
        mtim = time.time()
        if spd > 0: mcnt = mcnt + 1
        if spd < 0: mcnt = mcnt - 1
        mwri(mcnt,5,4)

# approximate frequencies: 0, 0.2, 0.3, 0.4, 0.5, 0.58, -0.58, -0.5, -0.4, -0.3, -0.2
serv = [1500, 1550, 1590, 1660, 1770, 2000, 1000, 1220, 1320, 1380, 1420]
# segments for digits 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, minus symbol and empty display
mnum=[0x7E,0x30,0x6D,0x79,0x33,0x5B,0x5F,0x70,0x7F,0x7B,0x01,0x00]

mypi=pigpio.pi()

cont = mypi.spi_open(0, 50000, 0)
mypi.spi_xfer(cont, [12, 1])      # turn on
mypi.spi_xfer(cont, [11, 7])      # show all
mypi.spi_xfer(cont, [10, 15])     # max intensity
for i in range(8):                # clear screen
    mypi.spi_xfer(cont, [i+1, 0])

mypi.set_mode(pimi, pigpio.INPUT)
mypi.set_mode(pipl, pigpio.INPUT)
mypi.set_mode(pire, pigpio.INPUT)
mypi.set_pull_up_down(piha, pigpio.PUD_OFF)
mypi.set_pull_up_down(pimi, pigpio.PUD_UP)
mypi.set_pull_up_down(pipl, pigpio.PUD_UP)
mypi.set_pull_up_down(pire, pigpio.PUD_UP)

mypi.set_servo_pulsewidth(pise, serv[0])
mwri(mcnt,5,4)
mwri(spd,1,2)

mypi.callback(piha, pigpio.RISING_EDGE, magn)

try:
    while True:
        # button controls
        if ((mypi.read(pimi) == 0) and (mypi.read(pipl) == 0) and (time.time()-butb > 0.5)):
            nspd = 0
            butb = time.time()
        if ((mypi.read(pimi) == 0) and (time.time()-buto > 0.5)):
            nspd = spd - 1
            if nspd < -5: nspd = -5
            buto = time.time()
        if ((mypi.read(pipl) == 0) and (time.time()-buto > 0.5)):
            nspd = spd + 1
            if nspd > 5: nspd = 5
            buto = time.time()
        if (mypi.read(pire) == 0):
            mcnt = 0
            mwri(mcnt,5,4)
    		
        # rotation speed control
        if nspd != spd:
            spd = nspd
            mypi.set_servo_pulsewidth(pise, serv[spd])
            mwri(spd,1,2)

except KeyboardInterrupt:
    mypi.set_servo_pulsewidth(pise, serv[0])
    for i in range(2):                # clear screen
        mypi.spi_xfer(cont, [i+1, 0])
