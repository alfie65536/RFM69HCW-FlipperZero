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

LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT

rfm69 = adafruit_rfm69.RFM69(spi, cs, reset, RADIO_FREQ_MHZ, sync_word= b"\xBB\xCC", preamble_length=4)

rfm69._write_u8(0x02, 0x08) #Enable OOK
rfm69._write_u8(0x37, 0x80) #Disable Whitening

rfm69.bitrate = 8333
rfm69.frequency_deviation = 0

print("Temperature: {0}C".format(rfm69.temperature))
print("Frequency: {0}mhz".format(rfm69.frequency_mhz))
print("Bit rate: {0}kbit/s".format(rfm69.bitrate / 1000))
print("Frequency deviation: {0}hz".format(rfm69.frequency_deviation))

while True:
    packet = rfm69.receive()
    if packet is None:
        LED.value = False
    else:
        if (send_up in packet):
            print("Up")
            print("poop")
        elif (send_down in packet):
            print("Down")
        elif (send_left in packet):
            print("Left")
        elif (send_right in packet):
            print("Right")
        elif (send_center in packet):
            print("Center")
        else:
            print("nah")
        LED.value = True
        
"""
uU5H2(.@vcXRxp - UP
M]85~n`=jqSU{P - DOWN
Sqe*p9<Yz?kms{ - LEFT
jN:nJ`6RLk@$9r - RIGHT
aDFSv:#]T?nJ8} - CENTER
"""

