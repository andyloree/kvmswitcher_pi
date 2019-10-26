#!/usr/bin/env python3
import sys
import threading
from signal import pause
from gpiozero import Button

NULL_CHAR = chr(0x00)
KEY_SCROLLLOCK = 0x47
PC1_BUTTON = "BOARD29" 
PC2_BUTTON = "BOARD31" 
PC3_BUTTON = "BOARD33"
PC4_BUTTON = "BOARD35"
keyLock = threading.Lock()

def SendKeyCode(packet):
        with open('/dev/hidg0', 'rb+') as fd:
                fd.write(packet.encode())

def SwitchKVM(number):
        numberKeys = {
                        'KEY_1': 0x1E,
                        'KEY_2': 0x1F,
                        'KEY_3': 0x20,
                        'KEY_4': 0x21
                }
        print("Sending PC " + number + " switch")
        # Scroll Lock
        SendKeyCode(NULL_CHAR*2 + chr(KEY_SCROLLLOCK) + NULL_CHAR*5)
        SendKeyCode(NULL_CHAR*8)
        # Scroll Lock
        SendKeyCode(NULL_CHAR*2 + chr(KEY_SCROLLLOCK) + NULL_CHAR*5)
        SendKeyCode(NULL_CHAR*8)
        # Number key for desired pc
        SendKeyCode(NULL_CHAR*2 + chr(numberKeys['KEY_' + number]) + NULL_CHAR*5)
        SendKeyCode(NULL_CHAR*8)


def main():
	print("Creating GPIO pin buttons")
	# PC1	
	pc1 = Button(PC1_BUTTON)
	pc1.when_pressed = lambda: SwitchKVM('1')
	# PC2	
	pc2 = Button(PC2_BUTTON)
	pc2.when_pressed = lambda: SwitchKVM('2') 
	# PC3	
	pc3 = Button(PC3_BUTTON)
	pc3.when_pressed = lambda: SwitchKVM('3')
	# PC4
	pc4 = Button(PC4_BUTTON)
	pc4.when_pressed = lambda: SwitchKVM('4')	
	print("Entering interrupt waiting for GPIO button presses")
	# Wait for a interrupt signal
	try:
		pause()
	except KeyboardInterrupt:
		pass

if __name__ == '__main__':
	main()
