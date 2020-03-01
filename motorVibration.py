from gpiozero import PWMOutputDevice
from time import sleep
import readMidiMido as midi
import constants

class VibrationMotor:

    # Constructor
    def __init__(self, pinNumber: int):
        self._vibrationMotor = PWMOutputDevice(pinNumber)

    def vibrate(self, vibrationValue: int):
        self._vibrationMotor.value = vibrationValue

    def calculateVibrationValue(self, value: int) -> int:
        pass
