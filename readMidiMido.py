from rtmidi import midiutil
from time import sleep
import time
import constants
import logging
import motorVibration as motor

class ReadMidi:
    
    def __init__(self, port: str):
        print("Constructor")
        self._midiIn, self._midiPort = midiutil.open_midiinput(port)
        self._motor = motor.VibrationMotor(constants.GPIO_PIN)
        # for motor in range constants.NUMBER_OF_MOTORS:

    @property
    def port(self):
        return self._midiPort
    
    @port.setter
    def port(self, port):
        self._midiPort = port


    @property
    def midiIn(self):
        return self._midiIn

    @midiIn.setter
    def midiIn(self, midiIn):
        self._midiIn = midiIn


    def list_input_ports(self):
        midiutil.list_input_ports()
    
    def _open_input_port(self):
        midiutil.open_midiinput(self._midiPort)

    
    def _get_midi_messages(self):
        try:
            timer = time.time()
            while True:
                msg = self._midiIn.get_message()
                if msg:
                    print("Message got")
                    message, deltatime = msg
                    timer += deltatime
                    print("message: %r, timer: @%0.6f" % (message, timer))
                    self._motor.vibrate(self._motor.calculateVibrationValue(message[0])) # see what part of message we need to take
                else:
                    self._motor.vibrate(0)
                time.sleep(0.01)
        except KeyboardInterrupt:
            print('')
        finally:
            self._midiIn.close_port()
            # print("Exit from midi reading")
    
    def toNote(self, number: int):
        pass
    
    def run(self):
        self._open_input_port()
        self._get_midi_messages()