# based on neopixel dust bag
# learn.adafruit.com/neopixel-pixie-dust-bag

import time
import board
import digitalio
import neopixel

try:
    import urandom as random  # for v1.0 API support
except ImportError:
    import random

neo_pin = board.A2  # DIGITAL IO pin for pixels
touch_pin = board.D2  # DIGITAL IO pin for momentary button
pixel_count = 50  # Number of LEDs connected trinket
delay_sec = .010  # delay between blinks, smaller numbers are faster
delay_mult = 8  # Randomization multiplier, delay speed of the effect

# initialize neopixels
pixels = neopixel.NeoPixel(neo_pin, pixel_count, brightness=.9, auto_write=False)

oldstate = False  # counting momentary button
showcolor = 0  # color mode for cycling

# initialize momentary button
button = digitalio.DigitalInOut(touch_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
PURPLE = (180, 0, 200)
WHITE = (255, 255, 255)
NONE = (0,0,0)

while True:

    rcolor = 100  # GOLD
    gcolor = 0
    bcolor = 0

    if showcolor == 3:  # ORANGE
        rcolor = 255
        gcolor = 100
        bcolor = 0

    newstate = button.value

    # Check if state changed (button press).
    if newstate and not oldstate:
        # give feedback to the Serial in MU to debug the touch pad
        print("Button Selection:", showcolor)

        if showcolor == 0: # WHITE
            pixels.fill(WHITE)
            pixels.write()

        if showcolor == 1: # SPARKLE GREEN-WHITE 
            pixels.fill(NONE)
            pixels.write()
            while button.value == newstate:
                # select a random pixel
                p = random.randint(0, (pixel_count - 2))
                # color value from momentary switch
                pixels[p] = WHITE
                pixels.write()
                # delay value randomized to up to delay_mult times longer
                time.sleep(delay_sec * random.randint(0, delay_mult))
                # set to a dimmed version of the state color
                pixels[p] = RED
                pixels.write()
                # set a neighbor pixel to an even dimmer value
                pixels[p + 1] = (int(200 / 15), 0, 0)
                pixels.write()

        if showcolor == 2: # WHITE
            pixels.fill(WHITE)
            pixels.write()

        if showcolor == 3:
            while button.value == newstate:
                #sparkling
                #select a random pixel
                p = random.randint(0, (pixel_count - 2))
                #color value from momentary switch
                pixels[p] = (rcolor, gcolor, bcolor)
                pixels.write()
                #delay value randomized to up to delay_mult times longer
                time.sleep(delay_sec * random.randint(0, delay_mult))
                # set to a dimmed version of the state color
                pixels[p] = (int(rcolor / 10), int(gcolor / 10), int(bcolor / 10))
                pixels.write()
                # set a neighbor pixel to an even dimmer value
                pixels[p + 1] = (int(rcolor / 15), int(gcolor / 15), int(bcolor / 15))
                pixels.write()

        if showcolor == 4: # WHITE
            pixels.fill(WHITE)
            pixels.write()

        if showcolor == 5: # PURPLE
            time.sleep(0.05)
            dim_by = 20
            pos = 0
            counter = 0
            PURPLE = (180, 0, 200)
            while button.value == newstate:
                if counter <= 50:
                    pixels[pos] = PURPLE
                    pixels[0:] = [[max(i-dim_by,0) for i in l] for l in pixels] # dim all by (dim_by,dim_by,dim_by)
                    pos = (pos+1) % 50 # move to next position
                    pixels.show()
                    counter = counter + 1
                    time.sleep(0.38)
                else:
                    pixels.fill(NONE)
                    pixels.write()

        if showcolor == 6: #flash on/off/on sparkle
            pixels.fill(WHITE)
            pixels.write()
            time.sleep(1)
            pixels.fill(NONE)
            pixels.write()
            time.sleep(1)
            pixels.fill(WHITE)
            pixels.write()
            time.sleep(1)
            rcolor = 255
            gcolor = 100
            bcolor = 0
            use = 0
            use1 = 0
            use2 = 0
            pixels.fill(NONE)
            pixels.write()
            while button.value == newstate:
                # sparkling
                # select a random pixel
                p = random.randint(0, (pixel_count-1))
                if pixels[p]:
                    use = random.randint(0,255)
                    use1 = random.randint(0,255)
                    use2 = random.randint(0,255)
                    pixels[p] = (use, use1, use2)
                    pixels.write()
                elif pixels[p:2]:
                    use = random.randint(0,255)
                    use1 = random.randint(0,255)
                    use2 = random.randint(0,255)
                    pixels[p:2] = (use, use1, use2)
                    pixels.write()
                elif pixels[p:3]:
                    use = random.randint(0,255)
                    use1 = random.randint(0,255)
                    use2 = random.randint(0,255)
                    pixels[p:3] = (use, use1, use2)
                else:
                    pixels = WHITE
                    pixels.write()
                time.sleep(delay_sec * random.randint(0, delay_mult))

        if showcolor == 7: #WHITE
            pixels.fill(WHITE)
            pixels.write()

        showcolor += 1

        # limit the cycle to the 5 colors
        if showcolor > 7:
            showcolor = 0

    # Set the last button state to the old state.
    oldstate = newstate
