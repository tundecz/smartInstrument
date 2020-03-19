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
    

    def _get_note_and_velocity(self, message):
        note = message[1]
        velocity = message[2]
        return note, velocity
    
    def _get_midi_messages(self):
        try:
            timer = time.time()
            while True:
                for message in self._midiIn:
                    bytes_array = message.bytes()
                    if(bytes_array[0] is not 248):
                        note, velocity = self._get_note_and_velocity(bytes_array)
                        ansi_note = self._toNote(note)
                        print("Note %d pressed with %d velocity" %(ansi_note, velocity))
                        self._motor.vibrate(1,note)
                time.sleep(0.01)
        except KeyboardInterrupt:
            print('')
        finally:
            self._midiIn.close_port()
            print("Exited from midi reading")
    
    def _toNote(self, number):
        return constants.NOTES[number % 12]
    
    def run(self):
        self.list_input_ports()
        self._get_midi_messages()