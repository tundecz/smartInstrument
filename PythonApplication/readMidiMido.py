import mido
from time import sleep
import time
from gpioPins import GPIO_PINS
import logging
from motorVibration import VibrationMotor
from helper import Helper
from constants import HOST, PORT, DEFAULT_VALUE_FOR_SLIDER
import bridge
from messages import MESSAGES, Message, DEFAULT_VALUES


class ReadMidi():
    
    def __init__(self, port):
        self._midiIn = mido.open_input(port)
        print(self._midiIn)

        # set gpio pins
        # self._bass_motors = VibrationMotor(GPIO_PINS.GPIO_PIN_14_BASS_CLEF.value)
        # self._treble_motors = VibrationMotor(GPIO_PINS.GPIO_PIN_15_TREBLE_CLEF.value)
        # self._upper_high_motors = VibrationMotor(GPIO_PINS.GPIO_PIN_18_HIGH_NOTES.value)

        self._bass_motors_1 = VibrationMotor(GPIO_PINS.GPIO_PIN_14_BASS_1.value)
        self._bass_motors_2 = VibrationMotor(GPIO_PINS.GPIO_PIN_15_BASS_2.value)
        self._bass_motors_3 = VibrationMotor(GPIO_PINS.GPIO_PIN_18_BASS_3.value)

        self._treble_motors_1 = VibrationMotor(GPIO_PINS.GPIO_PIN_17_TREBLE_1.value)
        self._treble_motors_2 = VibrationMotor(GPIO_PINS.GPIO_PIN_27_TREBLE_2.value)
        self._treble_motors_3 = VibrationMotor(GPIO_PINS.GPIO_PIN_22_TREBLE_3.value)

        self._high_motors_1 = VibrationMotor(GPIO_PINS.GPIO_PIN_10_HIGH_1.value)
        self._high_motors_2 = VibrationMotor(GPIO_PINS.GPIO_PIN_9_HIGH_2.value)
        self._high_motors_3 = VibrationMotor(GPIO_PINS.GPIO_PIN_11_HIGH_3.value)

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
            if DEFAULT_VALUES[Message.BASS] is True:
                frequency = Helper.convert_midi_number_to_frequency(note)
                value = Helper.calculate_value_based_on_note(note)
                self._put_frequency_in_array_for_client(frequency)
                self._bass_motors_2.vibrate(frequency, value)
                self._bass_motors_1.vibrate(frequency, value)
                self._bass_motors_3.vibrate(frequency, value)
        elif Helper.is_in_treble_range(note):
            print("Treble motor vibration")
            if DEFAULT_VALUES[Message.TREBLE] is True:
                frequency = Helper.convert_midi_number_to_frequency(note)
                value = Helper.calculate_value_based_on_note(note)
                self._put_frequency_in_array_for_client(frequency)
                self._treble_motors_1.vibrate(frequency, value)
                self._treble_motors_2.vibrate(frequency, value)
                self._treble_motors_3.vibrate(frequency, value)
        else:
            print("Upper high motors vibration")
            if DEFAULT_VALUES[Message.HIGH] is True:
                frequency = Helper.convert_midi_number_to_frequency(note)
                value = Helper.calculate_value_based_on_note(note)
                self._put_frequency_in_array_for_client(frequency)
                self._high_motors_1.vibrate(frequency, value)
                self._high_motors_2.vibrate(frequency, value)
                self._high_motors_3.vibrate(frequency, value)
    
    
    def _put_frequency_in_array_for_client(self, frequency):
        # put it if the client is connected
        if(DEFAULT_VALUES[Message.CONNECTED] == True):
            frequency_to_send = Helper.append_to_frequency(frequency)
            print(frequency_to_send)
            bridge.message_to_client_q.append(frequency_to_send)

    #stop motor vibration when not notes are coming
    def _stop_motors(self):
        self._stop_bass_motors()
        self._stop_treble_motors()
        self._stop_high_motors()
    
    # stop bass motors vibration
    # if we give 1 value, midi note will be 0
    def _stop_bass_motors(self):
        self._bass_motors_1.vibrate(0)
        self._bass_motors_2.vibrate(0)
        self._bass_motors_3.vibrate(0)
    
    # stop treble motor vibration
    def _stop_treble_motors(self):
        self._treble_motors_1.vibrate(0)
        self._treble_motors_2.vibrate(0)
        self._treble_motors_3.vibrate(0)

    # stop high motors vibration
    def _stop_high_motors(self):
        self._high_motors_1.vibrate(0)
        self._high_motors_2.vibrate(0)
        self._high_motors_3.vibrate(0)

    # we need to check if the event is set, then dequeue and check what command was passed
    # note_type = bass/treble/high/value
    # value = on/off/integer
    # default all the boolean params will be true
    # for the progress the parameter will be a value
    def _processEvent(self):
        message = bridge.dequeue_message()
        note_type, value = Helper.parse_dequeued_message(message)
        print("Message received in the readmidi class {}".format(message))
        if note_type == MESSAGES[Message.SWITCH]:
           self._setValues(value, Message.SWITCH)
        elif note_type == MESSAGES[Message.BASS]:
            self._setValues(value, Message.BASS)
        elif note_type == MESSAGES[Message.TREBLE]:
            self._setValues(value, Message.TREBLE)
        elif note_type == MESSAGES[Message.HIGH]:
            self._setValues(value, Message.HIGH)
        elif note_type == MESSAGES[Message.PROGRESS]:
            # need to convert because value is a string
            progress_value = int(value)
            print(progress_value)
            DEFAULT_VALUES[Message.PROGRESS] = progress_value
        elif note_type == MESSAGES[Message.RESET]:
            self._resetToDefaultValues()
            

    # set the values for DEFAULT_VALUE dictionary based on message got from Android application
    def _setValues(self, value, switch_type):
        print("In the set values method")
        print(str(value) + str(switch_type))
        if value == MESSAGES[Message.ON]:
            DEFAULT_VALUES[switch_type] = True
        elif value == MESSAGES[Message.OFF]:
            DEFAULT_VALUES[switch_type] = False

    def _resetToDefaultValues(self):
        DEFAULT_VALUES[Message.BASS] = True
        DEFAULT_VALUES[Message.TREBLE] = True
        DEFAULT_VALUES[Message.HIGH] = True
        DEFAULT_VALUES[Message.SWITCH] = True
        DEFAULT_VALUES[Message.PROGRESS] = DEFAULT_VALUE_FOR_SLIDER


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
                        if DEFAULT_VALUES[Message.SWITCH] is True: # for the case when the user stop or starts the device
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
    