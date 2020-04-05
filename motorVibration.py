from gpiozero import PWMOutputDevice
from time import sleep
import constants
from helper import Helper

class VibrationMotor:

    # Constructor
    def __init__(self, gpio):
        self._vibrationMotor = PWMOutputDevice(gpio)
        print("Hi from the motor constructor. GPIO 14 set.")

    # vibrate the motor with the calculated frequency and value
    def vibrate(self, velocity, midiNote = 0):
        # if we don't check if the note was pressed and we pass 0 to frequency converter
        # it may not work (calculation problems) => more safe this way
        if(midiNote is not constants.NOTE_OFF_VALUE):
            self._set_motor_value_and_frequency(velocity, midiNote)
            sleep(0.1)
        else:
           self._set_to_0()

    def _get_frequency_and_value(self, velocity, midiNote):
        try:
            frequency = Helper.convert_midi_number_to_frequency(midiNote)
        except Exception:
            print("Cannot convert to frequency")
        value = 1 # change this  to calculate from velocity
        return frequency, value
    
    # set the value to 0 and frequency to 100
    def _set_to_0(self):
        self._vibrationMotor.value = constants.NOTE_OFF_VALUE
        self._vibrationMotor.frequency = constants.DEFAULT_FREQUENNCY

    def _set_motor_value_and_frequency(self, velocity, midiNote):
        frequency, value = self._get_frequency_and_value(velocity, midiNote)
        self._vibrationMotor.value = value
        self._vibrationMotor.frequency = frequency
        print("vibrationValue: {}, frequency: {}".format(value, frequency))

    # desctructor
    def __del__(self):
        self._vibrationMotor.stop()