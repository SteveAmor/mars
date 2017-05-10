from gpiozero import MCP3008 # enable SPI using raspi-config
from gpiozero import Buzzer
from time import sleep
from os import system

buzzer = Buzzer(13)
adc = MCP3008(channel=0)

Vref = 3.3
potentialDividerMultiplier = 4.03 # Vin--10k--+--3.3k--GND
                                  #           |
                                  #           A0

while True:
    voltage = adc.value * Vref * potentialDividerMultiplier
    if voltage < 10: # 10V threshold to prevent battery damage
        for i in range (5):
            buzzer.on()
            sleep(0.5)
            buzzer.off()
            sleep(0.5)
        system("sudo shutdown now")
    else:
        buzzer.off()
    sleep(0.05)
