############################
# This code is started at boot up by crontab
# to edit crontab type: sudo crontab -e

# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

import time
import random

import Adafruit_MCP9808.MCP9808 as MCP9808

import Adafruit_BBIO.ADC as ADC

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import Image
import ImageDraw
import ImageFont

########## Display Setup ############################
# Beaglebone Black pin configuration:
RST = 'P9_12'
# Note the following are only used with SPI:
DC = 'P9_15'
SPI_PORT = 1
SPI_DEVICE = 0

# 128x64 display with hardware SPI:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Initialize library.
disp.begin()

# Get display width and height.
width = disp.width
height = disp.height

# Clear display.
disp.clear()
disp.display()

# Create image buffer.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (width, height))

# Load default font.
font = ImageFont.load_default()
#font = ImageFont.truetype('Minecraftia.ttf', 8)
#font = ImageFont.truetype('/var/lib/cloud9/Fonts/gunship_bitmap/GUNV2BM.FON', 16)
font = ImageFont.truetype('/var/lib/cloud9/Fonts/thirteen_pixel_fonts/thirteen_pixel_fonts.ttf', 24)
#font = ImageFont.truetype('/var/lib/cloud9/Fonts/bm_neco/BMNEA___.TTF', 16)
#font = ImageFont.truetype('/var/lib/cloud9/Fonts/pixel_freaks/PIXEL___.TTF', 23)


# Alternatively load a TTF font.
# Some nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

padding = 2
top = padding
x = padding

# Get display width and height.
width = disp.width
height = disp.height



########## Temp Sensor Setup ########################
senseP2 = 'P9_40'
 
ADC.setup()

# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
	return c * 9.0 / 5.0 + 32.0
	
# Define a function to read the TPM36 temp sensor
def tmp36Read():
    reading2 = ADC.read(senseP2)
    millivolts2 = reading2 * 1800  # 1.8V reference = 1800 mV
    temp_c2 = (millivolts2 - 450) / 10
    temp_f2 = (temp_c2 * 9/5) + 32
    return temp_f2

# Default constructor will use the default I2C address (0x18) and pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
#
# For the Beaglebone Black the library will assume bus 1 by default, which is
# exposed with SCL = P9_19 and SDA = P9_20.
sensor = MCP9808.MCP9808()

# Optionally you can override the address and/or bus number:
#sensor = MCP9808.MCP9808(address=0x20, busnum=2)

# Initialize communication with the sensor.
sensor.begin()

#########################################################
# Turn off the user LED's because they are bright and anyoing
# turn off USR0
open("/sys/class/leds/beaglebone:green:usr0/trigger", 'w').write("none")
open("/sys/class/leds/beaglebone:green:usr0/brightness", 'w').write("0")
# turn off USR1
open("/sys/class/leds/beaglebone:green:usr1/trigger", 'w').write("none")
open("/sys/class/leds/beaglebone:green:usr1/brightness", 'w').write("0")
# turn off USR2
open("/sys/class/leds/beaglebone:green:usr2/trigger", 'w').write("none")
open("/sys/class/leds/beaglebone:green:usr2/brightness", 'w').write("0")
# turn off USR3
open("/sys/class/leds/beaglebone:green:usr3/trigger", 'w').write("none")
open("/sys/class/leds/beaglebone:green:usr3/brightness", 'w').write("0") 

# Loop printing measurements every second.
print 'Press Ctrl-C to quit.'


#while True:
temp = sensor.readTempC()
#tmp36 = tmp36Read()


while True:
    # Clear display.
    # Clear image buffer by drawing a black filled box.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    time.sleep(0.1)
    temp = sensor.readTempC()
    tempF = c_to_f(temp)
    tmp36 = tmp36Read()  #read the TMP36 sensor connected to pin 40
    #text = 'Temp: {0:0.2F}*F'.format(tempF) + ' {0:0.2F}*F'.format(tmp36)
    text = '{0:0.1F}'.format(tmp36)
    xrand = random.randint(0,73)
    yrand = random.randint(0,36)
    print text
    #draw.text((x, top),    'Temp: {0:0.2F}*F'.format(tempF),  font=font, fill=255)
    #draw.text((x, top),    'Temp Monitor v 0.2',  font=font, fill=255)
    draw.text((x+xrand, top+yrand),    text,  font=font, fill=255)
    #draw.text((x+73, top+36),    text,  font=font, fill=255)
    #draw.text((x, top+40),  'Hello Owen', font = font, fill=128)
    #draw.text((x, top+50),  'Go Seahawks!!', font = font, fill=128)
    disp.image(image)
    disp.display()
    time.sleep(2.0)

# Clear display.
disp.clear()
disp.display()
