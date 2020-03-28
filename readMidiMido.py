import mido
from time import sleep
import time
import constants
import logging
from motorVibration import VibrationMotor
from helper import Helper

class ReadMidi:
    
    def __init__(self, port):
        print("Constructor")
        self._midiIn = mido.open_input(port)
        print(self._midiIn)
        self._motor = VibrationMotor()


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
            print("Something went wrong with byte parsing")

    # returns true if the array is a pressed note 
    # if no note was pressed, the array looks like this => [248]
    def _is_pressed_note(self, bytes_array):
        return True if bytes_array.__len__() > 1 else False

    # get the midi messages from the piano, convert them into bytes and send information to Vibration class
    def _get_midi_messages(self):
        try:
            timer = time.time()
            while True:
                for message in self._midiIn:
                    bytes_array = message.bytes()
                    if(self._is_pressed_note(bytes_array)):
                        note, velocity = self._get_note_and_velocity(bytes_array)
                        ansi_note = Helper.number_to_note(note)
                        print("Note %s pressed with %d velocity" %(ansi_note, velocity))
                        # self._motor.vibrate(1,note)
                    else:
                        pass
                        # self._motor.vibrate(0)
                time.sleep(0.01)
        except KeyboardInterrupt:
            print('Interrupted from keyboard\n')
        finally:
            self._close_input_port()
    
    # entry point from main class
    def run(self):
        self.list_input_ports()
        self._get_midi_messages()