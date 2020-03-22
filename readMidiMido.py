from rtmidi import midiutil
import mido
from time import sleep
import time
import constants
import logging
import motorVibration as motor
import helper

class ReadMidi:
    
    def __init__(self, port):
        print("Constructor")
        # self._midiIn, self._midiPort = midiutil.open_midiinput(port)
        self._midiIn = mido.open_input(port)
        print(self._midiIn)
        self._motor = motor.VibrationMotor()


    @property
    def midiIn(self):
        return self._midiIn

    @midiIn.setter
    def midiIn(self, midiIn):
        self._midiIn = midiIn


    def list_input_ports(self):
        # midiutil.list_input_ports()
        mido.get_input_names()

    def _close_input_port(self):
        self._midiIn.close()
        print("Midi port closed")
    

    def _get_note_and_velocity(self, message):
        try:
            note = message[1]
            velocity = message[2]
            return note, velocity
        except:
            print("Something went wrong with byte parsing")

    def _is_pressed_note(self, bytes_array):
        return True if bytes_array.__len__() > 1 else False

    
    def _get_midi_messages(self):
        try:
            timer = time.time()
            while True:
                for message in self._midiIn:
                    bytes_array = message.bytes()
                    if(self._is_pressed_note(bytes_array)):
                        note, velocity = self._get_note_and_velocity(bytes_array)
                        ansi_note = self._toNote(note)
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
    
    def _toNote(self, number):
        return constants.NOTES[number % 12]
    
    def run(self):
        self.list_input_ports()
        self._get_midi_messages()