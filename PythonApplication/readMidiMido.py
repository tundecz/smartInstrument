import mido
from time import sleep
import time
from gpioPins import GPIO_PINS
import logging
from motorVibration import VibrationMotor
from helper import Helper
from constants import HOST, PORT
import bridge
from messages import MESSAGES, Message


class ReadMidi():
    
    def __init__(self, port):
        self._midiIn = mido.open_input(port)
        print(self._midiIn)

        # set gpio pins
        self._bass_motors = VibrationMotor(GPIO_PINS.GPIO_PIN_14_BASS_CLEF.value)
        self._treble_motors = VibrationMotor(GPIO_PINS.GPIO_PIN_15_TREBLE_CLEF.value)
        self._upper_high_motors = VibrationMotor(GPIO_PINS.GPIO_PIN_18_HIGH_NOTES.value)

    @property
    def midiIn(self):
        return self._midiIn

    @midiIn.setter
    def midiIn(self, midiIn):
        self._midiIn = midiIn

    # get list of available input ports
    def list_input_ports(self):
        mido.get_input_names()

    # close input port
    def _close_input_port(self):
        self._midiIn.close()
        print("Midi port closed")
    

    # parsing the array and returning the values seperately
    def _get_note_and_velocity(self, message):
        try:
            note = message[1]
            velocity = message[2]
            return note, velocity
        except:
            print("Something went wrong with byte parsing\n")

    # returns true if the array is a pressed note 
    # if no note was pressed, the array looks like this => [248]
    def _is_pressed_note(self, bytes_array):
        return True if bytes_array.__len__() > 1 else False
    
    # check for midi number to see what set of motors shoudl vibrate
    def _vibrate_the_motors(self, note, velocity):
        if Helper.is_in_bass_range(note):
            print("Bass motor vibration")
            self._bass_motors.vibrate(velocity, note)
        elif Helper.is_in_treble_range(note):
            print("Treble motor vibration")
            self._treble_motors.vibrate(velocity, note)
        else:
            print("Upper high motors vibration")
            self._upper_high_motors.vibrate(velocity, note)
    
    #stop motor vibration when not notes are coming
    def _stop_motors(self):
        self._bass_motors.vibrate(0)
        self._treble_motors.vibrate(0)
        self._upper_high_motors.vibrate(0)

    # we need to check if the event is set, then dequeue and check what command was passed
    # note_type = bass/treble/high/value
    # value = on/off/integer
    def _processEvent(self):
        message = bridge.dequeue_message()
        note_type, value = Helper.parse_dequeued_message(message)
        print("Message received in the readmidi class {}".format(message))
        if note_type is MESSAGES[Message.BASS]:
            if value is MESSAGES[Message.ON]:
                pass
            elif value is MESSAGES[Message.OFF]:
                pass
        elif note_type is MESSAGES[Message.TREBLE]:
            if value is MESSAGES[Message.ON]:
                pass
            elif value is MESSAGES[Message.OFF]:
                pass
        elif note_type is MESSAGES[Message.HIGH]:
            if value is MESSAGES[Message.ON]:
                pass
            elif value is MESSAGES[Message.OFF]:
                pass
        elif note_type is MESSAGES[Message.PROGRESS]:
            progress_value = int(value)


    # get the midi messages from the piano, convert them into bytes and send information to Vibration class
    def _get_midi_messages(self):
        try:
            while True:
                for message in self._midiIn:
                    if bridge.ev.is_set():
                        self._processEvent()
                    bytes_array = message.bytes()
                    if(self._is_pressed_note(bytes_array)):
                        note, velocity = self._get_note_and_velocity(bytes_array)
                        ansi_note = Helper.number_to_note(note)
                        print("Note %s pressed with %d velocity" %(ansi_note, velocity))
                        self._vibrate_the_motors(note, velocity)
                    else:
                        self._stop_motors()
        except KeyboardInterrupt:
            print('Interrupted from keyboard\n')
        finally:
            self._close_input_port()
    
    # entry point from main class
    def run(self):
        self.list_input_ports()
        self._get_midi_messages()