from microbit import *
import microbit
import math

# optional opening sequence, a series of images is displayed,
# the matrix represents the led display, 0 off, 9 max on
display.show(Image('00000:'
                   '00000:'
                   '00900:'
                   '00900:'
                   '00900'))
sleep(100)
display.show(Image('00000:'
                   '00000:'
                   '00900:'
                   '09090:'
                   '90009'))
sleep(100)
display.show(Image('00000:'
                   '00000:'
                   '99999:'
                   '00000:'
                   '00000'))
sleep(100)
display.show(Image('90009:'
                   '09090:'
                   '00900:'
                   '00000:'
                   '00000'))
sleep(100)
display.show(Image('00900:'
                   '00900:'
                   '00900:'
                   '00000:'
                   '00000'))
sleep(100)
display.show(Image('00000:'
                   '00000:'
                   '00000:'
                   '00000:'
                   '00000'))
sleep(100)
display.show(Image('00900:'
                   '00900:'
                   '00900:'
                   '00000:'
                   '00000'))
sleep(100)
display.show(Image('90009:'
                   '09090:'
                   '00900:'
                   '00000:'
                   '00000'))
sleep(100)
display.show(Image('00000:'
                   '00000:'
                   '99999:'
                   '00000:'
                   '00000'))
sleep(100)
display.show(Image('00000:'
                   '00000:'
                   '00900:'
                   '09090:'
                   '90009'))
sleep(100)
display.show(Image('00000:'
                   '00000:'
                   '00900:'
                   '00900:'
                   '00900'))
sleep(100)
display.show(Image('00000:'
                   '00000:'
                   '00300:'
                   '00900:'
                   '00900'))
sleep(200)
display.show(Image('00000:'
                   '00000:'
                   '00000:'
                   '00300:'
                   '00900'))
sleep(200)
display.show(Image('00000:'
                   '00000:'
                   '00000:'
                   '00000:'
                   '00300'))
sleep(200)
# open lid, place lid on strata, rotate compass till display is
# horizontal,
# led should converge to centre when compass is horizontal
# note that Microbit is mounted reversed to allow usb access
# Measure dip direction while pushing button A continuously.
# value is plotted in led matrix,
# first row 100's
# second row 00 - 50
# third row 60 - 90
# fourth row 0 - 5
# fifth row 6 - 9
# measure dip angle:
# Place compass on side on strata, parallel to dip direction with lid full open
# dip angle is measured while button B is pushed
# dip = tan (gy/gx) (integer and always positive)
# calibrate compass before measurement, push A and B simultaneously


# SETTINGS
# POWERSAVE set brightness between 1 and 9 for brightness leds (9 is max)
# brightness 9 is ok in bright sunlight
brightness = 9
# MEASURE STRIKE instead of dip dir (default) strike is true strike is displayed
# strike = false
# MAGNETIC DECLINATION set magnetic declination decl in degrees,
# eastwards is positive, westwards is negative (not implemented yet)
decl = 0

def bargraph(a):
    # note display is reversed in this version
    # plot value (a) as bars on led display (a is max 499)
    # split a in 100's, 10's and 1's
    a100 = a // 100
    a10 = (a % 100)//10
    a1 = (a % 10)
    a15 = a10 - 5
    a5 = a1 - 5
    display.clear()
    # optional send value a to REPL
    # print(str("a="), a)
    for y in range(0, 5):
        if a100 > y:
            # for x in range(0, 5):
                display.set_pixel(4, y, brightness)
        if a10 > y:
                display.set_pixel(3, y, brightness)
        if a15 > y:
                display.set_pixel(2, y, brightness)
        if a1 > y:
                display.set_pixel(1, y, brightness)
        if a5 > y:
                display.set_pixel(0, y, brightness)

# calibrate before use, measurement triggers calibration if nessesary
# microbit.compass.calibrate()
# test = microbit.compass.heading()

while True:
    gx = microbit.accelerometer.get_x()
    gy = microbit.accelerometer.get_y()
    # gz = microbit.accelerometer.get_z()
    # new code here, define ly
    if gy < -100:
        ly = 0
    elif gy < -16:
        ly = 1
    elif gy > 100:
        ly = 4
    elif gy > 16:
        ly = 3
    else:
        ly = 2

    if gx > 100:
        display.clear()
        display.set_pixel(4, ly, 9)
    elif gx > 16:
        display.clear()
        display.set_pixel(3, ly, 9)
    elif gx < -100:
        display.clear()
        display.set_pixel(0, ly, 9)
    elif gx < -16:
        display.clear()
        display.set_pixel(1, ly, 9)
    else:
        display.clear()
        display.set_pixel(2, ly, 9)

    while microbit.button_a.is_pressed() and not microbit.button_b.is_pressed():
        hd = microbit.compass.heading()
        # correct for mounting in 3d case
        # microbit bearing to top
        # so dipdir is hd, no correction
        # add or subtract 90 for strike, then check if hd not > 360
        hd = hd + 0
        # if hd > 360:
        #    hd = hd - 360
        hd = hd + decl
        # plot the result using bargraph routine
        bargraph(round(hd))

    while microbit.button_b.is_pressed() and not microbit.button_a.is_pressed():
        # place microbit on side and measure dipangle (gy/gx)
        gx = microbit.accelerometer.get_x()
        gy = microbit.accelerometer.get_y()
        # dipanglerad = math.atan(abs(gy/gx))
        # mounting at 0 deg
        # Gx can be zero
        if gx == 0:
            gx = gx + 1
        dipanglerad = math.atan(abs(gy/gx))
        dipangledeg = dipanglerad * 57.296
        sleep(100)
        bargraph(round(dipangledeg))
        # re-callibrate when A and B pressed
    while microbit.button_a.is_pressed() and microbit.button_b.is_pressed():
        microbit.compass.calibrate()
        sleep(200)
        break