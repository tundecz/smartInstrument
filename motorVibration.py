from gpiozero import PWMOutputDevice
from time import sleep
import constants
from helper import Helper

class VibrationMotor:

    # Constructor
    def __init__(self):
        self._vibrationMotor = PWMOutputDevice(constants.GPIO_PIN_14)

    # set the vibration value and frequency
    # default frequency is 100  Hz
    # we need midiNote to calculate the frequency
    def vibrate(self, vibrationValue, midiNote):
        frequency = Helper.convertMidiNumberToFrequency(midiNote)
        self._vibrationMotor.value = vibrationValue
        self._vibrationMotor.frequency = frequency

    # desctructor
    def __del__(self):
        self._vibrationMotor.stop()
