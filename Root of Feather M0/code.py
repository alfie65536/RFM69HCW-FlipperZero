# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple example to send a message and then wait indefinitely for messages
# to be received.  This uses the default RadioHead compatible GFSK_Rb250_Fd250
# modulation and packet format for the radio.
import board
import busio
import digitalio
import time

import adafruit_rfm69

#Variables

send_up = b"uU5H2(.@vcXRxp"
send_down = b"M]85~n`=jqSU{P"
send_left = b"Sqe*p9<Yz?kms{"
send_right = b"jN:nJ`6RLk@$9r"
send_center = b"aDFSv:#]T?nJ8}"

#Initiate RFM69HCW
RADIO_FREQ_MHZ = 433.92

cs = digitalio.DigitalInOut(board.RFM69_CS)
reset = digitalio.DigitalInOut(board.RFM69_RST)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

#LED = digitalio.DigitalInOut(board.D13)
#LED.direction = digitalio.Direction.OUTPUT

rfm69 = adafruit_rfm69.RFM69(spi, cs, reset, RADIO_FREQ_MHZ, sync_word= b"\xBB\xCC", preamble_length=4)

rfm69._write_u8(0x02, 0x08) #Enable OOK
rfm69._write_u8(0x37, 0x80) #Disable Whitening

rfm69.bitrate = 8333
rfm69.frequency_deviation = 0

print("Temperature: {0}C".format(rfm69.temperature))
print("Frequency: {0}mhz".format(rfm69.frequency_mhz))
print("Bit rate: {0}kbit/s".format(rfm69.bitrate / 1000))
print("Frequency deviation: {0}hz".format(rfm69.frequency_deviation))

#Fun Test Stuff
LED = digitalio.DigitalInOut(board.D10)
LED2 = digitalio.DigitalInOut(board.D9)

LED.direction = digitalio.Direction.OUTPUT
LED2.direction = digitalio.Direction.OUTPUT

LED.value = True
LED2.value = True

onoff = 0

LED.value = False
LED2.value = False


while True:
    packet = rfm69.receive()
    if packet is not None:
        if (send_up in packet):
            LED.value = True
        elif (send_down in packet):
            LED2.value = True
        elif (send_left in packet):
            LED.value = False
        elif (send_right in packet):
            LED2.value = False
        elif (send_center in packet):
            if (onoff == 0):
                LED.value = True
                LED2.value = True
                onoff = 1
            elif (onoff == 1):
                LED.value = False
                LED2.value = False
                onoff = 0